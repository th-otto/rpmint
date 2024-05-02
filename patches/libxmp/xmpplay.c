/* A simple frontend for libxmp */
/* This file is in public domain */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <SDL/SDL.h>
#include <xmp.h>


static char const progname[] = "xmpplay";

static int playing;
static SDL_AudioSpec a;
#ifndef XMP_FORMAT_BYTESWAP
static int must_swap;
#endif


static void fill_audio(void *udata, Uint8 *stream, int len)
{
#ifndef XMP_FORMAT_BYTESWAP
	if (must_swap)
	{
		Uint16 *p = udata;
		int count = len >> 1;
		while (--count >= 0)
		{
			*p = __builtin_bswap16(*p);
			p++;
		}
	}
#endif
	if (xmp_play_buffer((xmp_context) udata, stream, len, 0) < 0)
		playing = 0;
}


static int sdl_init(xmp_context ctx)
{
	if (SDL_Init(SDL_INIT_AUDIO | SDL_INIT_NOPARACHUTE) < 0)
	{
		fprintf(stderr, "sdl: can't initialize: %s\n", SDL_GetError());
		return -1;
	}

	if (SDL_OpenAudio(&a, NULL) < 0)
	{
		fprintf(stderr, "%s\n", SDL_GetError());
		return -1;
	}

	return 0;
}


static void sdl_deinit(void)
{
	SDL_CloseAudio();
}


static void usage(void)
{
	fprintf(stderr, "Usage: %s [-8] [-r rate] [-c channels] [-m] <module>\n", progname);
}


int main(int argc, char **argv)
{
	xmp_context ctx;
	struct xmp_module_info mi;
	struct xmp_frame_info fi;
	int i;

	ctx = xmp_create_context();

	a.freq = 44100;
	a.format = AUDIO_S16SYS;
	a.channels = 0;
	a.samples = 0;
	a.callback = fill_audio;
	a.userdata = ctx;

	/* Check command line usage */
	for (i = 1; i < argc && argv[i][0] == '-'; ++i)
	{
		if (strcmp(argv[i], "-r") == 0 && (i + 1) < argc)
		{
			++i;
			a.freq = atoi(argv[i]);
		} else if (strcmp(argv[i], "-m") == 0 )
		{
			a.channels = 1;
		} else if (strcmp(argv[i], "-c") == 0 && (i + 1) < argc)
		{
			++i;
			a.channels = atoi(argv[i]);
		} else if (strcmp(argv[i], "-8") == 0)
		{
			a.format = AUDIO_U8;
		} else
		{
			usage();
			return EXIT_FAILURE;
		}
	}

	if (sdl_init(ctx) < 0)
	{
		fprintf(stderr, "%s: can't initialize sound\n", progname);
		return EXIT_FAILURE;
	}

	for (; i < argc; i++)
	{
		int format;
		
		if (xmp_load_module(ctx, argv[i]) < 0)
		{
			fprintf(stderr, "%s: error loading %s\n", progname, argv[i]);
			continue;
		}

		format = 0;
		if ((a.format & 0xff) > 8)
		{
			if (((a.format ^ AUDIO_S16SYS) & 0x1000) != 0)
			{
#ifdef XMP_FORMAT_BYTESWAP
				format |= XMP_FORMAT_BYTESWAP;
#else
				must_swap = 1;
#endif
			}
		} else
		{
			format |= XMP_FORMAT_8BIT;
		}
		if (!(a.format & 0x8000))
			format |= XMP_FORMAT_UNSIGNED;
		if (a.channels == 1)
			format |= XMP_FORMAT_MONO;

		if (xmp_start_player(ctx, a.freq, format) == 0)
		{
			int row;

			/* Show module data */

			xmp_get_module_info(ctx, &mi);
			printf("%s (%s)\n", mi.mod->name, mi.mod->type);

			/* Play module */

			playing = 1;
			SDL_PauseAudio(0);

			row = -1;
			while (playing)
			{
#ifdef __MINT__
				SDL_Delay(20);
#else
				usleep(20000);
#endif
				xmp_get_frame_info(ctx, &fi);
				if (fi.row != row)
				{
					printf("\r%3d/%3d %3d/%3d", fi.pos, mi.mod->len, fi.row, fi.num_rows);
					fflush(stdout);
					row = fi.row;
				}
			}
			xmp_end_player(ctx);
		}

		xmp_release_module(ctx);
		printf("\n");
	}

	xmp_free_context(ctx);

	sdl_deinit();

	return EXIT_SUCCESS;
}

<?php
declare(strict_types=1);

define('RELEASE_DIR', 'release');
define('DIR_SEP', "/");


class past_mistakes {
	/*
	 * packages with historical versions containing a hyphen, or other illegal
	 * character
	 */
	public static $illegal_char_in_version = array(
		'ctorrent' => ['1.3.4-dnh3.2'],
		'email' => ['3.2.1-git', '3.2.3-git'],
		'email-debuginfo' => ['3.2.1-git', '3.2.3-git'],
		'fdupes' => ['1.50-PR2'],
		'gendef' => ['1.0-svn2931'],
		'gendef-debuginfo' => ['1.0-svn2931'],
		'gt5' => ['1.5.0~20111220+bzr29'],
		'hidapi' => ['0.8.0-rc1'],
		'hidapi-debuginfo' => ['0.8.0-rc1'],
		'libhidapi-devel' => ['0.8.0-rc1'],
		'libhidapi0' => ['0.8.0-rc1'],
		'libmangle' => ['1.0-svn2930'],
		'libmangle-debuginfo' => ['1.0-svn2930'],
		'man-pages-posix' => ['2013-a'],
		'mingw64-i686-hidapi' => ['0.8.0-rc1'],
		'mingw64-i686-hidapi-debuginfo' => ['0.8.0-rc1'],
		'mingw64-x86_64-hidapi' => ['0.8.0-rc1'],
		'mingw64-x86_64-hidapi-debuginfo' => ['0.8.0-rc1'],
		'recode' => ['3.7-beta2'],
		'recode-debuginfo' => ['3.7-beta2'],
	);

	/*
	 * cygport places this into the requires of every debuginfo package, including
	 * cygwin-debuginfo itself
	 */
	public static $self_requires = [
		'cygwin-debuginfo' => true,
	];

	/* provides: which don't exist */
	public static $nonexistent_provides = [
		'_windows' => true,
		'perl5_026' => true,
		'rdiff-debuginfo' => true,
		'rxvt-unicode-X-debuginfo' => true,
		'xfce4-mixer-debuginfo' => true,
		'python3-dbus-debuginfo' => true,
	];

	/* provides: which don't exist and packages which require them should be expired */
	public static $expired_provides = [
		'python26' => true,
	];

	/*
	 * empty source packages
	 *
	 * (these usually have a corresponding hand-built empty install package, which
	 * depends on it's replacement, and so are a lingering remnant of something not
	 * properly obsoleted)
	 */
	public static $empty_source = [
		'catgets-src' => ['2.10.0-1'],
		'octave-octcdf-src' => ['1.1.7-99'],
		'perl-File-Slurp-Unicode-src' => ['0.7.1-2'],  /* obsoleted by perl-File-Slurp */
		'perl-Carp-src' => [ '1.38-2' ],               /* not really empty but too small */
		'python3-src' => [ '3.9.10-1', '3.8.6-1' ],    /* not really empty but too small */
		'vala-dconf' => [ '*' ],                       /* not really empty but too small */
		'vala-pkcs11' => [ '*' ],                      /* not really empty but too small */
	];

	/* these are packages which only contain data, symlinks or scripts and thus
	   function as their own source
	 */
	public static $self_source = [
		'R_autorebase' => true,
		'_update-info-dir' => true,
		'base-cygwin' => true,
		'chere' => true,
		'cygcheck-dep' => true,
	];

	/*
	 * these are packages which currently have versions different to all the other
	 * install packages from the same source package
	 *
	 * don't add to this list, use 'disable-check: unique-version' in pvr.hint instead
	 */
	public static $nonunique_versions = [
		'bzr-debuginfo' => true,			  /* debuginfo from NMU needs to age out */
		'cgdb-debuginfo' => true,			  /* debuginfo from NMU needs to age out */
		'dolphin4' => true, 				  /* dropped from kde-baseapps */
		'gcc-java' => true, 				  /* dropped from gcc 6 */
		'girepository-SpiceClientGtk2.0' => true,  /* gtk2 dropped from spice-gtk */
		'gnome-panel-doc' => true,
		'gtk2.0-engines-svg' => true,
		'kdepasswd' => true,				  /* dropped from split kde-baseapps */
		'kexi' => true, 					  /* split out from calligra */
		'kfilereplace' => true, 			  /* split out from kdewebdev */
		'libcaca-doc' => true,				  /* dropped pending fix for current doxygen */
		'libfltk-doc' => true,
		'libgcj-common' => true,			  /* dropped from gcc 6 */
		'libical_cxx-devel' => true,
		'libquota-devel' => true,			  /* no longer provided by e2fsprogs */
		'libtxc_dxtn' => true,				  /* split out from s2tc */
		'mingw64-i686-poppler-qt4' => true,   /* dropped since 0.62.0 */
		'mingw64-i686-spice-gtk2.0' => true,  /* gtk2 dropped from spice-gtk */
		'mingw64-x86_64-poppler-qt4' => true, /* dropped since 0.62.0 */
		'mingw64-x86_64-spice-gtk2.0' => true, /* gtk2 dropped from spice-gtk */
		'minizip' => true,
		'mutter-doc' => true,
		'ocaml-camlp4' => true, 			  /* ocaml-camlp4 removed from ocaml distribution after 4.01.0 */
		'okular4-part' => true, 			  /* changed to okular5-part in 17.04 */
		'python-spiceclientgtk' => true,	  /* gtk2 dropped from spice-gtk */
		'sng-debuginfo' => true,
		'sqlite3-zlib' => true, 			  /* sqlite3-zlib removed in 3.8.10, use sqlite3-compress instead */
		'w3m-img' => true,
	];

	/*
	 * empty install packages, that aren't obsolete
	 *
	 * don't add to this list, use 'disable-check: empty-obsolete' in pvr.hint instead
	 */
	public static $empty_but_not_obsolete = [
		'isl' => ['0.16.1-1'],									 /* useless empty package, not autosupressed as it has depends */
		'libpopt-devel' => ['1.16-1'],							 /* version 1.16-1 was empty (x86_64) */
		'libpopt0' => ['1.16-1'],								 /* version 1.16-1 was empty */
		'mbedtls' => ['2.16.0-1'],								 /* useless empty package, not autosupressed as it has depends */
		'mpclib' => ['1.1.0-1'],								 /* useless empty package, not autosupressed as it has depends */
		'mpfr' => ['4.0.2-1'],									 /* useless empty package, not autosupressed as it has depends */
		'serf-debuginfo' => ['1.3.8-1', '1.3.9-1'], 			 /* empty presumably due to build problems */
	];

	/*
	 * packages with timestamp anomalies
	 *
	 * don't add to this list, use 'disable-check: curr-most-recent' in override.hint instead
	 */
	public static $mtime_anomalies = [
		'gcc-tools-epoch2-autoconf' => true,
		'gcc-tools-epoch2-autoconf-src' => true,
	];

	/*
	 * packages with maintainer anomalies
	 *
	 * don't add to this list, fix the package
	 */
	public static $maint_anomalies = [
		'manlint' => ['1.6g-2'],  /* unclear why this is under man */
		'python3-h5py-debuginfo' => ['2.9.0-1'],  /* superceded by python-h5py-debuginfo */
	];

	/*
	 * packages missing obsoletions
	 *
	 * don't add to this list, fix the package (e.g. by adding the needed obsoletions)
	 * (an enhancement to cygport might be necessary to support doing that for
	 * debuginfo packages?)
	 */
	public static $missing_obsolete = [
		'filemanager-actions-debuginfo' => ['caja-actions-debuginfo'],
		'guile2.2-debuginfo' => ['guile-debuginfo'],
		'librsync-debuginfo' => ['rdiff-debuginfo'],
		'man-db-debuginfo' => ['man-debuginfo'],		/* contain conflicting files */
		'procps-ng' => ['procps'],
		'procps-ng-debuginfo' => ['procps-debuginfo'],	/* contain conflicting files */
		'python2-debuginfo' => ['python-debuginfo'],	/* contain conflicting files */
		'python-dbus-debuginfo' => ['python3-dbus-debuginfo'],
		'rxvt-unicode-debuginfo' => ['rxvt-unicode-X-debuginfo'],
		'spectacle-debuginfo' => ['ksnapshot-debuginfo'],
		'xfce4-pulseaudio-plugin-debuginfo' => ['xfce4-mixer-debuginfo'],
		'xfig-debuginfo' => ['transfig-debuginfo'], 	/* contain conflicting files */
	];

	public static $short_ldesc = [
		'gnupg' => true,
	];
};


function safe_opendir(string $filename) #: \resource
{
	$report = error_reporting();
	error_reporting($report & ~E_WARNING);
	$dh = opendir($filename);
	error_reporting($report);
	return $dh;
}


function safe_file(string $filename) : array|false
{
	$report = error_reporting();
	error_reporting($report & ~E_WARNING);
	$lines = file($filename);
	error_reporting($report);
	return $lines;
}


class SetupVersion {
	public string $version_string;
	public string $epoch;
	public string $version;
	public string $release;

	public function __construct(string $version_string)
	{
		$this->_version_string = $version_string;

		/* split release on the last '-', if any (default '') */
		$vr = explode('-', $version_string, 2);
		$v = array_shift($vr);
		$r = empty($vr) ? '' : $vr[0];

		/* split epoch, on the first ':', if any (default '0') */
		$ev = explode(':', $v, 2);
		if (count($ev) === 2)
		{
			$e = $ev[0];
			$v = $ev[1];
		} else
		{
			$e = '0';
		}
		$this->epoch = $e;
		$this->version = $v;
		$this->release = $r;

		/*
		 * then split each part into numeric and alphabetic sequences
		 * non-alphanumeric separators are discarded
		 * numeric sequences have leading zeroes discarded
		 */
		$this->_epoch = self::splitv($this->epoch);
		$this->_version = self::splitv($this->version);
		$this->_release = self::splitv($this->release);

		/*
		echo("string: $version_string\n");
		echo("v: {$this->version} [" . join(', ', $this->_version) . "]\n");
		echo("r: {$this->release} [" . join(', ', $this->_release) . "]\n");
		echo("e: {$this->epoch} [" . join(', ', $this->_epoch) . "]\n");
		echo("\n");
		*/
	}

	private static function splitv(string $s): array
	{
		preg_match_all('/(\d+|[a-zA-Z]+|[^a-zA-Z\d]+)/', $s, $sequences, PREG_PATTERN_ORDER);
		$sequences = $sequences[1];
		foreach ($sequences as $i => $s)
			if (preg_match('/[^a-zA-Z\d]+/', $s))
				unset($sequences[$i]);
			else
				$sequences[$i] = preg_replace('/^0+(\d)/', '\1', $sequences[$i]);
		/* reorder any deleted keys */
		return explode('|', join('|', $sequences));
	}


	public static function compare(SetupVersion $a, SetupVersion $b): int
	{
		/* compare E */
		$c = self::_compare($a->_epoch, $b->_epoch);
		if ($c !== 0)
			return $c;
		/* compare V */
		$c = self::_compare($a->_version, $b->_version);
		if ($c !== 0)
			return $c;

		/* if V are the same, compare R */
		return self::_compare($a->_release, $b->_release);
	}

	public static function reverse_compare(SetupVersion $a, SetupVersion $b): int
	{
		return -self::compare($a, $b);
	}

	public function __toString(): string
	{
		return "{$this->version_string} (E={$this->epoch} V={$this->version} R={$this->release})";
	}

	public function __lt(SetupVersion $other): bool
	{
		return $this->__cmp($other) < 0;
	}

	public function __eq(SetupVersion $other): bool
	{
		return $this->__cmp($other) === 0;
	}

	public function __cmp(SetupVersion $other): int
	{
		return self::compare($this, $other);
	}

	/* comparison helper function */
	public static function _compare(array $a, array $b): int
	{
		$len = min(count($a), count($b));
		for ($i = 0; $i < $len; $i++)
		{
			/* sort a non-digit sequence before a digit sequence */
			if (ctype_digit($a[$i][0]) !== ctype_digit($b[$i][0]))
				return ctype_digit($a[$i]) ? 1 : -1;
			/* compare as numbers */
			if (ctype_digit($a[$i]))
			{
				/* because leading zeros have already been removed, if one number */
				/* has more digits, it is greater */
				$c = strlen($a[$i]) <=> strlen($b[$i]);
				if ($c !== 0)
					return $c;
			}
			/* compare lexicographically */
			$c = $a[$i] <=> $b[$i];
			if ($c !== 0)
				return $c;
		}
		/* if equal length, all components have matched, so equal */
		/* otherwise, the version with a suffix remaining is greater */
		return count($a) <=> count($b);
	}

}



/* a path inside a package repository (e.g relative to relarea) */
class RepoPath {
	public ?string $arch;
	public ?string $pkgpath;
	public ?string $filename;

	public function __construct(?string $arch, ?string $path, ?string $filename)
	{
		$this->arch = $arch;
		$this->pkgpath = $path;
		$this->filename = $filename;
	}

	/* convert to a path, absolute if given a base directory */
	public function abspath(string $basedir = null): string
	{
		$pc = $this->pkgpath . DIR_SEP . $this->filename;
		if ($basedir !== null)
			$pc = $basedir . DIR_SEP . $pc;
		return $pc;
	}

	/* convert to a MoveList tuple */
	public function move(): array
	{
		return array($this->pkgpath, $this->filename);
	}
}


/* kinds of hint file, and their allowed keys */
enum HintType: int {
	case pvr = 0;
	case spvr = 1;
	case override = 2;
}


/* information we keep about a hint file */
class Hint {
	public RepoPath $repopath;
	public array $hints;

	/*
	 * types of key:
	 * 'multilineval' - always have a value, which may be multiline
	 * 'val'		  - always have a value
	 * 'optval' 	  - may have an empty value
	 * 'noval'		  - always have an empty value
	 */
	private static $keytypes = ['multilineval', 'val', 'optval', 'noval', 'multi'];
	private static bool $licensing = false;

	private static array $hintkeys = [
		0 /* HintType::pvr->value */ => [
			'ldesc' => 'multilineval',
			'category' => 'multi',
			'sdesc' => 'val',
			'test' => 'noval',	 /* mark the package as a test version */
			'version' => 'val',  /* version override */
			'disable-check' => 'multi',
			'notes' => 'val',	 /* tool notes; not significant to calm itself */
			'message' => 'multilineval',
			'external-source' => 'val',
			'requires' => 'multi',
			'obsoletes' => 'multi',
			'provides' => 'multi',
			'conflicts' => 'multi',
		],

		1 /* HintType::spvr->value */ => [
			'ldesc' => 'multilineval',
			'category' => 'multi',
			'sdesc' => 'val',
			'test' => 'noval',	 /* mark the package as a test version */
			'version' => 'val',  /* version override */
			'disable-check' => 'multi',
			'notes' => 'val',	 /* tool notes; not significant to calm itself */
			'skip' => 'noval',	 /* in all spvr hints, but ignored */
			'homepage' => 'val',
			'build-depends' => 'multi',
			'license' => 'val',
		],

		2 /* HintType::override->value */ => [
			'keep' => 'val',
			'keep-count' => 'val',
			'keep-count-test' => 'val',
			'keep-days' => 'val',
			'keep-superseded-test' => 'noval',
			'disable-check' => 'multi',
			'replace-versions' => 'multi',
			'noretain' => 'val',
		],
	];

	/* valid categories */
	public static array $categories = [
		'accessibility' => true,
		'admin' => true,
		'archive' => true,
		'audio' => true,
		'base' => true,
		'comm' => true,
		'database' => true,
		'debug' => true,
		'devel' => true,
		'doc' => true,
		'editors' => true,
		'games' => true,
		'gnome' => true,
		'graphics' => true,
		'interpreters' => true,
		'kde' => true,
		'libs' => true,
		'lua' => true,
		'lxde' => true,
		'mail' => true,
		'mate' => true,
		'math' => true,
		'net' => true,
		'ocaml' => true,
		'office' => true,
		'perl' => true,
		'php' => true,
		'publishing' => true,
		'python' => true,
		'ruby' => true,
		'scheme' => true,
		'science' => true,
		'security' => true,
		'shells' => true,
		'source' => true,  /* added to all source packages created by deduplicator to ensure they have a category */
		'sugar' => true,
		'system' => true,
		'tcl' => true,
		'text' => true,
		'utils' => true,
		'video' => true,
		'virtual' => true,
		'web' => true,
		'x11' => true,
		'xfce' => true,
		'_obsolete' => true,
	];

	public function __construct(?string $arch, ?string $path, ?string $filename)
	{
		$this->repopath = new RepoPath($arch, $path, $filename); /* pathname of hint file */
		$this->hints = []; /* XXX: duplicates version_hints, for the moment */
	}

	private static function item_lexer(array &$lines, int &$i, string &$item, string &$error) : bool
	{
		if ($i >= count($lines))
			return false;

		$line = $lines[$i];
		$i++;
		$item = '';
		$error = '';
		/* validate that .hint file is UTF-8 encoded */
		if (mb_detect_encoding($line, "UTF-8") !== "UTF-8")
		{
			$error = 'invalid UTF-8';
			return true;
		}

		/* discard lines starting with '#' */
		if (str_starts_with($line, '#'))
			return true;

		/* discard empty lines */
		$line = trim($line);
		if ($line === '')
			return true;

		/* line containing quoted text */
		$quotations = substr_count($line, '"');
		if ($quotations === 2)
		{
			$item = $line;
			return true;
		}

		/* if the line contains an opening quote */
		if ($quotations === 1)
		{
			while ($i < count($lines))
			{
				/*
				 * multi-line quoted text preserves any leading space used for
				 * indentation, but removes any trailing space
				 */
				$line = $line . "\n" . rtrim($lines[$i]);
				$i++;
				/* multi-line quoted text is only terminated by a quote at the */
				/* end of the line */
				if (str_ends_with($line, '"'))
				{
					$item = $line;
					return true;
				}
			}
			$item = $line;
			$error = "unterminated quote";
			return true;
		}

		/* an unquoted line */
		$item = $line;
		return true;
	}

	public static function file_parse(string $pn, string $filename, ?HintType $kind, bool $strict): ?array
	{
		$errors = [];
		$warnings = [];
		$hints = [];
		$i = 0;
		$item = '';
		$error = '';

		if (($lines = safe_file($filename)) === false)
			return null;

		/* parse as key:value items */
		while (self::item_lexer($lines, $i, $item, $error))
		{
			if ($error !== '')
				$errors[] = "$error at line $i";
			if ($item == '')
				continue;

			$quotations = substr_count($item, '"');
			if ($quotations !== 0 && $quotations !== 2)
				$errors[] = "double-quote within double-quotes at line $i (hint files have no escape character)";

			if (preg_match('/^([^:\s]+):\s*(.*)$/s', $item, $match)) /* PCRE_DOTALL */
			{
				$key = $match[1];
				$value = $match[2];
				if ($kind !== null)
				{
					if (!isset(self::$hintkeys[$kind->value][$key]))
					{
						$errors[] = "unknown key $key at line $i";
						continue;
					}
					$valtype = self::$hintkeys[$kind->value][$key];
					/* check if the key occurs more than once */
					if (isset($hints[$key]) && $valtype !== 'multi')
						$errors[] = "duplicate key $key at line $i";

					/* check the value meets any key-specific constraints */
					if ($valtype === 'val' && $value === '')
						$errors[] = "$key has empty value";

					if ($valtype === 'noval' && $value !== '')
						$errors[] = "$key has non-empty value '$value'";

					/* only 'ldesc' and 'message' are allowed a multi-line value */
					if ($valtype !== 'multilineval'  && substr_count($value, "\n") > 0)
						$errors[] = "key $key has multi-line value";
				}

				/* validate all categories are in the category list (case-insensitively) */
				if ($key === 'category')
				{
					foreach (preg_split('/[\s]/', $value, 0, PREG_SPLIT_NO_EMPTY) as $c)
					{
						$c = strtolower(trim($c));
						if (!isset(self::$categories[$c]))
							$errors[] = "unknown category '$c'";
					}
				}

				/* verify that value for ldesc or sdesc is quoted (genini forces this) */
				if ($key === 'sdesc' || $key === 'ldesc')
				{
					if (!str_starts_with($value, '"') || !str_ends_with($value, '"'))
						$errors[] = "$key value should be quoted";

					/* warn about and fix common typos in ldesc/sdesc */
					list($value, $msg) = self::typofix($value);
					if (!empty($msg))
						$warnings[] = join(',', $msg) . " in $key";
				}

				/* if sdesc ends with a '.', warn and fix it */
				if ($key === 'sdesc')
				{
					if (substr($value, -2) === '."')
					{
						$warnings[] = "$key ends with '.'";
						$value = substr($value, 0, -2) . '"';
					}
				}

				/* if sdesc contains '	', warn and fix it */
				if ($key === 'sdesc')
				{
					if (strpos($value, '  ') !== false)
					{
						$warnings[] = "$key contains '	'";
						$value = str_replace('	', ' ', $value);
					}
				}

				/* message must have an id and some text */
				if ($key === 'message')
				{
					if (!preg_match('/(\S+)\s+(\S.*)/', $value))
						$errors[] = "$key value must have id and text";
				}

				/* license must be a valid spdx license expression */
				if ($key === 'license' && self::$licensing)
				{
				}

				/* warn if value starts with a quote followed by whitespace */
				if (preg_match('/^"[ \t]+/', $value))
					$warnings[] = "value for key $key starts with quoted whitespace";

				/* store the key:value */
				if ($valtype === 'multi')
				{
					/* strip off any version relation enclosed in '()' following the package name */
					if (preg_match_all('/([^\s,(]+),?[\s]*(\([^)]*\))?/', $value, $match, PREG_SET_ORDER) !== false)
					{
						foreach ($match as $m)
						{
							/* remove any extraneous whitespace */
							$c = trim($m[0]);
							$hints[$key][$m[1]] = $c;
						}
					} else
					{
						$errors[] = "$key: invalid value $value";
					}
				} else
				{
					$hints[$key] = $value;
				}
			} else
			{
				$errors[] = "unknown construct '$item' at line $i";
			}
		}

		if (isset($hints['skip']) && count($hints) === 1)
			$errors[] = "hint only contains skip: key, please update to cygport >= 0.22.0";

		/* for the pvr kind, 'category' and 'sdesc' must be present */
		/* (genini also requires 'requires' but that seems wrong) */
		/* for the spvr kind, 'homepage' must be present for new packages */
		if ($kind === HintType::pvr || $kind === HintType::spvr)
		{
			if (!isset($hints['category']))
			   $errors[] = "required key 'category' missing";
			if (!isset($hints['sdesc']))
			   $errors[] = "required key 'sdesc' missing";
			if ($kind === HintType::spvr && $strict && !isset($hints['homepage']))
			   $errors[] = "required key 'sdesc' missing";

			if ($kind === HintType::spvr && $strict)
				if (!isset($hints['license']))
					$warnings[] = "key 'license' missing";
		}

		/*
		 * warn if ldesc and sdesc seem transposed
		 *
		 * (Unfortunately we can't be totally strict about this, as some
		 * packages like to repeat the basic description in ldesc in every
		 * subpackage, but add to sdesc to distinguish the subpackages)
		 */
		if (isset($hints['ldesc']))
			if (strlen($hints['sdesc']) > 2 * strlen($hints['ldesc']) && !isset(past_mistakes::$short_ldesc[$pn]))
				$warnings[] = 'sdesc is much longer than ldesc';

		/* sort these hints, as differences in ordering are uninteresting */
		if (isset($hints['build-depends']))
			ksort($hints['build-depends'], SORT_STRING);
		
		if (isset($hints['obsoletes']))
			ksort($hints['obsoletes'], SORT_STRING);

		if (isset($hints['replace-versions']))
			ksort($hints['replace-versions'], SORT_STRING);

		if (!empty($errors))
			$hints['parse-errors'] = $errors;

		if (!empty($warnings))
			$hints['parse-warnings'] = $warnings;

		return $hints;
	}

	/*
	 * words that package maintainers apparently can't spell correctly
	 */
	private static $words = [
		[' accomodates ', ' accommodates '],
		[' consistant ', ' consistent '],
		[' examing ', ' examining '],
		[' extremly ', ' extremely '],
		[' interm ', ' interim '],
		[' procesors ', ' processors '],
		[' utilitzed ', ' utilized '],
		[' utilties ', ' utilities '],
	];


	private static function typofix(string $value): array
	{
		$msg = [];
		foreach (self::$words as list($wrong, $right))
		{
			if (strpos($value, $wrong) !== false)
			{
				$value = str_replace($wrong, $right, $value);
				$msg[] = trim($wrong) . " -> " . trim($right);
			}
		}
		return [$value, $msg];
	}
}


/* kinds of packages */
enum PkgKind: int {
	case binary = 0;
	case source = 1;
	case all = 2;
}

/* information we keep about a package */
class Package {
	public string $pkgpath;
	public array $tarfiles; /* of Tar object */
	public array $hints;	/* of Hint object */
	public array $is_used_by; /* of package names */
	public array $version_hints;
	public ?array $override_hints;
	public bool $not_for_output;
	public PkgKind $kind;
	public string $name;
	public string $orig_name;
	public bool $has_requires;
	public bool $obsolete;
	public array $rdepends; /* of Package object */
	public array $build_rdepends; /* of Package object */
	public array $obsoleted_by; /* of Package object */
	public bool $orphaned;
	public ?string $best_version;

	public function __construct()
	{
		$this->pkgpath = ''; /* path to package, relative to arch */
		$this->tarfiles = array();
		$this->hints = array();
		$this->is_used_by = array();
		$this->version_hints = array();
		$this->override_hints = null;
		$this->not_for_output = false;
		$this->kind = PkgKind::binary;
	}

	public function tar(string $vr): ?Tar
	{
		if (isset($this->tarfiles[$vr]))
			return $this->tarfiles[$vr];
		return null;
	}

	public function versions(): array
	{
		return $this->tarfiles;
	}

	public function srcpackage(string $vr, bool $suffix = true)
	{
		if ($this->kind === PkgKind::source)
		{
			$spn = $this->name;
		} else
		{
			/* source tarfile is in the external-source package, if specified, */
			/* otherwise it's in the sibling source package */
			$hints = [];
			if (isset($this->version_hints[$vr]))
				$hints = $this->version_hints[$vr];
			if (isset($hints['external-source']))
				$spn = $hints['external-source'];
			else
				$spn = $this->name . '-src';
		}
		if (!$suffix)
			if (str_ends_with($spn, "-src"))
				$spn = substr($spn, 0, -4);
		return $spn;
	}

	public function __toString(): string
	{
		return sprintf("Package('%s', %s, %s, %s, %s)", $this->pkgpath, join(' ', array_keys($this->tarfiles)), join(' ', array_keys($this->version_hints)), join(' ', array_keys($this->override_hints)), $this->not_for_output);
	}
}


/* information we keep about a tar file */
class Tar {
	public RepoPath $repopath;
	public string $sha512;
	public int $size;
	public int $mtime;
	public bool $is_empty;
	public bool $is_used;
	public bool $sourceless;
	private SetupVersion $version;

	public function __construct(string $arch, string $path, string $filename, string $version_string)
	{
		$this->repopath = new RepoPath($arch, $path, $filename);
		$this->sha512 = '';
		$this->size = 0;
		$this->mtime = 0;
		$this->is_empty = false;
		$this->is_used = false;
		$this->version = new SetupVersion($version_string);
	}

	/*
	 * utility to determine if a tar file is empty
	 */
	public function tarfile_is_empty(string $pn): bool
	{
		/*
		 * report invalid files (smaller than the smallest possible compressed file
		 * for any of the compressions we support)
		 */
		if ($this->size < 14)
		{
			mksetup::error_log("tar archive {$this->filename} is too small ({$this->size} bytes)");
			$this->is_empty = true;
		} else if ($this->size < 32)
		{
			/*
			 * sometimes compressed empty files are used rather than a compressed empty
			 * tar archive
			 */
			$this->is_empty = true;
		} else if ($this->size > 1024)
		{
			/*
			 * parsing the tar archive just to determine if it contains at least one
			 * archive member is relatively expensive, so we just assume it contains
			 * something if it's over a certain size threshold
			 */
			$this->is_empty = false;
		} else
		{
			if (isset(past_mistakes::$empty_source[$pn]))
				$this->is_empty = false;
			else
				$this->is_empty = true;
		}
		return $this->is_empty;
	}

	public static function compare(Tar $a, Tar $b): int
	{
		return SetupVersion::compare($a->version, $b->version);
	}

	public static function reverse_compare(Tar $a, Tar $b): int
	{
		return SetupVersion::reverse_compare($a->version, $b->version);
	}

	public function __toString(): string
	{
		return sprintf("Tar('%s', '%s', '%s', %d, %s)", $this->repopath->filename, $this->repopath->pkgpath, $this->sha512, $this->size, $this->is_empty);
	}
}


function array_update(array &$dst, ?array $values): void
{
	if ($values === null)
		return;
	if ($dst === null)
		$dst = [];
	foreach ($values as $key => $value)
		$dst[$key] = $value;
}


class packages {
	private string $arch;
	private string $releasearea;
	private array $packages;  /* of Package object */

	public function __construct(string $releasearea, string $arch)
	{
		$this->releasearea = $releasearea;
		$this->arch = $arch;
	}

	private function read_hints(string $pn, string $vr, string $filename, HintType $kind, bool $strict = false): ?array
	{
		$hints = hint::file_parse($pn, $this->releasearea . DIR_SEP . $filename, $kind, $strict);
		if (isset($hints['parse-errors']))
		{
			foreach ($hints['parse-errors'] as $l)
				mksetup::error_log("package '$pn' version $vr: $l");
			return null;
		}
		if (isset($hints['parse-warnings']))
		{
			foreach ($hints['parse-warnings'] as $l)
				mksetup::error_log("package '$pn' version $vr: $l");
		}

		/*
		 * generate depends: from requires:
		 */
		if (isset($hints['requires']))
		{
			$hints['depends'] = $hints['requires'];
			ksort($hints['depends'], SORT_STRING);
			/* erase requires:, to ensure there is nothing using it */
			unset($hints['requires']);
		}
		return $hints;
	}


	/* helper function to clean up hints */
	private function clean_hints(string $pn, array $hints, bool &$warnings): void
	{
		/*
		 * fix some common defects in the hints
		 *
		 * don't allow a redundant 'package:' or 'package - ' at start of sdesc
		 *
		 * match case-insensitively, and use a base package name (trim off any
		 * leading 'lib' from package name, remove any soversion or 'devel'
		 * suffix)
		 */
		if (isset($hints['sdesc']))
		{
			if (preg_match('/^"(.*?)(\s*:|\s+-)/', $hints['sdesc'], $colon))
			{
				$package_basename = preg_replace('/^lib(.*?)(|-devel|\d*)$/', '\1', $pn);
				if (str_starts_with(strtoupper($package_basename), strtoupper($colon[1])))
				{
					mksetup::error_log("package '$pn' sdesc starts with '{$colon[1]}{$colon[2]}'; this is redundant as the UI will show both the package name and sdesc");
					$warnings = true;
				}
			}
		}
	}


	/*
	 * read a single package
	 */
	private function read_one_package(array &$packages, string $pn, string $relpath, array $files, PkgKind $kind, bool $upload): bool
	{
		$warnings = false;

		mksetup::debug("reading " . ($kind === PkgKind::source ? "source" : "binary") . " package $pn from $relpath: " . join(' ', $files));
		if (!preg_match('/^[\w\-._+]*$/', $pn))
		{
			mksetup::error_log("package '$pn' name contains illegal characters");
			return false;
		}
		/*
		 * assumption: no real package names end with '-src'
		 *
		 * enforce this, because source and install package names exist in a
		 * single namespace currently, and otherwise there could be a collision
		 */
		if (str_ends_with($pn, "-src"))
		{
			mksetup::error_log("package '$pn' name ends with '-src'");
			return false;
		}

		/* check for duplicate package names at different paths */
		[$arch, $release, $pkgpath] = explode(DIR_SEP, $relpath, 3);
		$spn = $pn;
		if ($kind === PkgKind::source)
			$spn .= '-src';
		if (isset($packages[$spn]))
		{
			mksetup::error_log("duplicate package name $pn at paths $relpath and {$packages[$spn]->pkgpath}");
			return false;
		}

		if (isset($files['override.hint']))
		{
			/* read override.hint */
			$filename = $relpath . DIR_SEP . 'override.hint';
			$override_hints = $this->read_hints($pn, '', $filename, HintType::override);
			if ($override_hints === null)
			{
				mksetup::error_log("error parsing $filename");
				return false;
			}
			unset($files['override.hint']);
		} else
		{
			$override_hints = null;
		}

		/*
		 * build a list of version-releases (since replacement pvr.hint files are
		 * allowed to be uploaded, we must consider both .tar and .hint files for
		 * that), and collect the attributes for each tar file
		 */
		$tars = array();
		$vr_list = array();

		foreach ($files as $f)
		{
			/*
			 * warn if filename doesn't follow P-V-R naming convention
			 *
			 * P must match the package name, V can contain anything, R must
			 * start with a number and can't include a hyphen
			 */
			if (!preg_match('/^' . preg_quote($pn) . '-(.+)-(\d[0-9a-zA-Z._+]*)(-src|)\.(tar\.(bz2|gz|lzma|xz|zst)|hint)$/', $f, $match))
			{
				mksetup::error_log("file '$f' in package '$pn' doesn't follow naming convention");
				return false;
			}
			$v = $match[1];
			$r = $match[2];
			/*
			 * historically, V can contain a '-' (since we can use the fact
			 * we already know P to split unambiguously), but this is a bad
			 * idea.
			 */
			if (strpos($v, '-') !== false)
			{
				if (!isset(past_mistakes::$illegal_char_in_version[$pn]))
				{
					mksetup::error_log("file '$f' in package '$pn' contains '-' in version");
					$warnings = true;
				}
			}
			if (!ctype_digit($v[0]))
			{
				mksetup::error_log("file '$f' in package '$pn' has a version which doesn't start with a digit");
				$warnings = true;
			}
			if (!preg_match('/^[\w\-._+]*$/', $v))
			{
				if (!isset(past_mistakes::$illegal_char_in_version[$pn]))
				{
					mksetup::error_log("file '$f' in package '$pn' has a version which illegal characters");
					$warnings = true;
				}
			}

			/* if not there already, add to version-release list */
			$vr = "$v-$r";
			$vr_list[] = $vr;

			if (!str_ends_with($f, ".hint"))
			{
				/* a package can only contain tar archives of the appropriate type */
				if (strpos($f, '-src.tar') === false)
				{
					if ($kind === PkgKind::source)
					{
						mksetup::error_log("source package '$pn' has install archives");
						return false;
					}
				} else
				{
					if ($kind === PkgKind::binary)
					{
						mksetup::error_log("package '$pn' has source archives");
						return false;
					}
				}

				/*
				 * for each version, a package can contain at most one tar file (of
				 * the appropriate type). Warn if we have too many (for e.g. both a
				 * .xz and .bz2 install tar file).
				 */
				if (isset($tars[$vr]))
				{
					mksetup::error_log("package '$pn' has more than one tar file for version '$vr'");
					return false;
				}

				/* collect the attributes for each tar file */
				$t = new Tar($arch, $relpath, $f, $vr);
				$filename = $this->releasearea . DIR_SEP . $relpath . DIR_SEP . $f;
				if (($stat = stat($filename)) !== false)
				{
					$t->size = $stat['size'];
					$t->mtime = $stat['mtime'];
					$t->tarfile_is_empty($pn);
					$t->sha512 = $this->sha512_file($filename);
				}
				$tars[$vr] = $t;
			}
		}

		/* determine hints for each version we've encountered */
		$version_hints = [];
		$hints = [];
		$actual_tars = [];

		foreach ($vr_list as $vr)
		{
			$hint_fn = $pn . "-" . $vr . ($kind === PkgKind::source ? "-src" : "") . ".hint";
			if (isset($files[$hint_fn]))
			{
				/* is there a PVR.hint file? */
				$filename = $relpath . DIR_SEP . $hint_fn;
				$pvr_hint = $this->read_hints($pn, $vr, $filename, $kind === PkgKind::binary ? HintType::pvr : HintType::spvr);
				if ($pvr_hint === null)
				{
					mksetup::error_log("error parsing $filename");
					return false;
				}
				$this->clean_hints($pn, $pvr_hint, $warnings);
			} else
			{
				/* it's an error to not have a pvr.hint */
				mksetup::error_log("package $pn has packages for version $vr, but no $hint_fn");
				return false;
			}

			/* apply a version override */
			if (isset($pvr_hint['version']))
			{
				$ovr = pvr_hint['version'];
				/* also record the version before the override */
				$pvr_hint['original-version'] = $vr;
			} else
			{
				$ovr = $vr;
			}
			/* external source will always point to a source package */
			if (isset($pvr_hint['external-source']))
				$pvr_hint['external-source'] .= '-src';

			$hintobj = new Hint($arch, $relpath, $hint_fn);
			$hintobj->hints = $pvr_hint;

			$version_hints[$ovr] = $pvr_hint;
			$hints[$ovr] = $hintobj;
			if (isset($tars[$vr]))
				$actual_tars[$ovr] = $tars[$vr];
		}

		$package = new Package();
		$package->name = $spn;
		$package->version_hints = $version_hints;
		$package->override_hints = $override_hints;
		$package->tarfiles = $actual_tars;
		$package->hints = $hints;
		$package->pkgpath = $relpath;
		$package->kind = $kind;
		/*
		 * since we are kind of inventing the source package names, and don't
		 * want to report them, keep track of the real name
		 */
		$package->orig_name = $pn;
		$packages[$spn] = $package;

		return !$warnings;
	}


	/*
	 * helper function to determine sha512 for a particular file
	 *
	 * read sha512 checksum from a sha512.sum file, if present, otherwise compute it
	 */
	private function sha512_file(string $filename): string
	{
		$dirname = dirname($filename);
		$basename = basename($filename);
		$sum_fn = $dirname . DIR_SEP . 'sha512.sum';
		$sha512 = $this->sha512sum_file_read($sum_fn);
		if ($sha512 === null)
		{
			mksetup::debug("no sha512.sum in $dirname");
		} else
		{
			if (isset($sha512[$basename]))
				return $sha512[$basename];
			mksetup::debug("no line for file $basename in checksum file $sum_fn");
		}
		$sha512 = hash_file('sha512', $filename);
		mksetup::debug("computed sha512 hash for $basename is $sha512");
		return $sha512;
	}


	/* helper function to parse a sha512.sum file */
	private function sha512sum_file_read(string $sum_fn): ?array
	{
		if (($lines = file($sum_fn)) === false)
			return null;
		$sha512 = array();
		foreach ($lines as $line)
		{
			if (preg_match('/^(\S+)\s+(?:\*|)(\S+)$/', $line, $match))
				$sha512[$match[2]] = $match[1];
			else
				mksetup::error_log("warning: bad line '$line' in checksum file $sum_fn");
		}
		return $sha512;
	}


	/*
	 * read a single package directory
	 *
	 * (may contain at most one source package and one binary package)
	 * (return True if problems, False otherwise)
	 */
	private function read_package_dir(array &$packages, string $relpath, int $depth, bool $upload = false): bool
	{
		$result = true;

		if (($dh = safe_opendir($this->releasearea . DIR_SEP . $relpath)) !== false)
		{
			$fl = array(
				PkgKind::binary->value => array(),
				PkgKind::source->value => array(),
				PkgKind::all->value => array(),
			);
			$hints_found = false;
			$files_found = false;
			/* the package name is always the directory name */
			$p = basename($relpath);
			while (($file = readdir($dh)) !== false)
			{
				if ($file !== "." && $file !== "..")
				{
					if ($relpath === '')
						$relfile = $file;
					else
						$relfile = $relpath . DIR_SEP . $file;
					mksetup::debug("processing $relfile");
					if (is_dir($this->releasearea . DIR_SEP . $relfile))
					{
						if (!$this->read_package_dir($packages, $relfile, $depth + 1, $upload))
						{
							$result = false;
						}
					} else if (is_file($this->releasearea . DIR_SEP . $relfile))
					{
						$files_found = true;
						/* ignore dotfiles, backup files and checksum files */
						if (!str_starts_with($file, ".") && !str_ends_with($file, ".bak") && $file !== "sha512.sum")
						{
							/* classify files for which kind of package they belong to */
							if ($file === "override.hint")
							{
								$fl[PkgKind::all->value][$file] = $file;
								$hints_found = true;
							} else if (str_starts_with($file, $p) && str_ends_with($file, ".hint"))
							{
								if (str_ends_with($file, "-src.hint"))
									$fl[PkgKind::source->value][$file] = $file;
								else
									$fl[PkgKind::binary->value][$file] = $file;
								$hints_found = true;
							} else if (str_starts_with($file, $p) && preg_match('/\.tar\.(bz2|gz|lzma|xz|zst)$/', $file))
							{
								if (strpos($file, '-src.tar') !== false)
									$fl[PkgKind::source->value][$file] = $file;
								else
									$fl[PkgKind::binary->value][$file] = $file;
							} else
							{
								/* warn about unexpected files, including tarfiles which don't match the package name */
								mksetup::error_log("unexpected file $relfile");
							}
						}
					} else
					{
						if (is_link($this->releasearea . DIR_SEP . $relfile))
							mksetup::error_log("dangling symlink $relfile");
						else
							mksetup::error_log("ignoring unknown file $relfile");
						$result = false;
					}
				}
			}
			closedir($dh);

			if (!$hints_found)
			{
				if ($files_found && $depth > 0)
				{
					mksetup::error_log("no .hint files in {$this->releasearea}/$relpath but has files");
					return false;
				}
				return $result;
			}

			/* read package */
			foreach ([PkgKind::binary, PkgKind::source] as $kind)
			{
				/* only create a package if there's archives for it to contain */
				if (!empty($fl[$kind->value]))
					if (!$this->read_one_package($packages, $p, $relpath, array_merge($fl[$kind->value], $fl[PkgKind::all->value]), $kind, $upload))
						$result = false;
			}
			return $result;
		} else
		{
			mksetup::error_log(error_get_last()['message']);
			return false;
		}
	}

	/*
	 * read packages from a directory hierarchy
	 */
	public function read_packages() : bool
	{
		$status = true;
		$this->packages = array();

		/* <arch>/ noarch/ and src/ directories are considered */
		foreach (array('noarch', 'src', $this->arch) as $root)
		{
			$this->packages[$root] = array();
			$releasedir = $this->releasearea . DIR_SEP . $root;
			mksetup::verbose("reading packages from ${releasedir}");
			if (!$this->read_package_dir($this->packages[$root], $root . DIR_SEP . RELEASE_DIR, 0))
				$status = false;
			mksetup::verbose(count($this->packages[$root]) . " packages read from ${releasedir}");
		}

		if (!$this->merge())
			$status = false;

		return $status;
	}


	/*
	 * merge sets of packages
	 *
	 * for each package which exist in both a and b:
	 * - they must exist at the same relative path
	 * - we combine the list of tarfiles, duplicates are not permitted
	 * - we use the hints from b, and warn if they are different to the hints for a
	 */
	private function merge(): bool
	{
		$status = true;
		$c = [];

		foreach ($this->packages as $arch)
		{
			foreach ($arch as $pn => $p)
			{
				/* if the package is in arch but not in a, add it to the copy */
				if (!isset($c[$pn]))
				{
					$c[$pn] = $p;
				} else
				{
					/* else, if the package is both in a and b, we have to do a merge */

					/* package must be of the same kind */
					if ($c[$pn]->kind !== $p->kind)
					{
						mksetup::error_log("package '$pn' is of more than one kind");
						return false;
					}
					/* package must exist at same relative path */
					if ($c[$pn]->pkgpath !== $p->pkgpath)
					{
						mksetup::error_log("package '$pn' is at paths {$c[$pn]->pkgpath} and {$p->pkgpath}");
						return false;
					}

					foreach ($p->tarfiles as $vr => $tar)
					{
						if (isset($c[$pn]->tarfiles[$vr]))
						{
							mksetup::error_log("package '$pn' has duplicate tarfile for version $vr");
							return false;
						}
						$c[$pn]->tarfiles[$vr] = $tar;
					}

					/* hints from arch override hints from a, but warn if they have changed */
					foreach ($p->version_hints as $vr => $val)
					{
						$c[$pn]->version_hints[$vr] = $val;
					}

					/* overrides from arch take precedence */
					array_update($c[$pn]->override_hints, $p->override_hints);

					/* merge hint file lists */
					array_update($c[$pn]->hints, $p->hints);
				}
			}
		}

		$this->packages = $c;

		return $status;
	}


	/*
	 * validate the package database
	 */
	public function validate(array $opt, array $valid_provides_extra = null, array $missing_obsolete_extra = null) : bool
	{
		$status = true;

		if ($this->packages === null)
			return true;

		if ($missing_obsolete_extra === null)
			$missing_obsolete_extra = [];

		/* build the set of valid things to depends: on */
		$valid_requires = [];

		foreach ($this->packages as $pn => $p)
		{
			$valid_requires[$pn] = true;
			foreach ($p->version_hints as $hints)
				if (isset($hints['provides']))
					foreach ($hints['provides'] as $pr)
						$valid_requires[$pr] = true;

			/* reset computed package state */
			$p->has_requires = false;
			$p->obsolete = false;
			$p->rdepends = [];
			$p->build_rdepends = [];
			$p->obsoleted_by = [];
			$p->orphaned = false;
			$p->is_used_by = [];
		}

		/* it's also valid to obsoletes: packages which have been removed */
		$valid_obsoletes = $valid_requires;
		if ($valid_provides_extra !== null)
			array_update($valid_obsoletes, $valid_provides_extra);

		/* perform various package validations */
		foreach ($this->packages as $pn => $p)
		{
			foreach ($p->version_hints as $v => $hints)
			{
				foreach ([
					['depends', 'missing-depended-package', $valid_requires],
					['obsoletes', 'missing-obsoleted-package', $valid_obsoletes]
				] as list($c, $okmissing, $valid))
				{
					/* if c is in hints, and not empty */
					if (isset($hints[$c]) && !empty($hints[$c]))
					{
						foreach ($hints[$c] as $r => $constraint)
						{
							if ($c === 'depends')
								/* don't count cygwin-debuginfo for the purpose of */
								/* checking if this package has any requires, as */
								/* cygport always makes debuginfo packages require */
								/* that, even if they are empty */
								if ($r !== 'cygwin-debuginfo')
									$p->has_requires = true;

							/* a package should not appear in it's own hint */
							if ($r === $pn)
							{
								if (!isset(past_mistakes::$self_requires[$pn]))
									mksetup::error_log("warning: package '$pn' version '$v' $c itself");
							}

							/* all packages listed in a hint must exist (unless the */
							/* disable-check option says that's ok) */
							if (!isset($valid[$r]) && !isset(array_merge(past_mistakes::$nonexistent_provides, past_mistakes::$expired_provides)[$r]))
							{
								if (!isset($opt['disable-check'][$okmissing]))
								{
									/* its ok to obsolete a removed package */
									if ($c !== 'obsoletes')
									{
										mksetup::error_log("package '$pn' version '$v' $c: '$r', but nothing satisfies that");
										$status = false;
									}
								}
								continue;
							}

							/* package relation hint referencing a source package makes no sense */
							if (isset($this->packages[$r]) && $this->packages[$r]->kind === PkgKind::source)
							{
								mksetup::error_log("package '$pn' version '$v' $c source package '$r'");
								$status = false;
							}
						}
					}
				}

				/* if external-source is used, the package must exist */
				if (isset($hints['external-source']))
				{
					$e = $hints['external-source'];
					if (!isset($this->packages[$e]))
					{
						mksetup::error_log("package '$pn' version '$v' refers to non-existent or errored external-source '$e'");
						$status = false;
					}
				}

				/* some old packages are missing needed obsoletes:, add them where */
				/* needed, and make sure the uploader is warned if/when package is */
				/* updated */
			}
		}

		$mo = array_merge(past_mistakes::$missing_obsolete, $missing_obsolete_extra);
		foreach ($mo as $pn => $val)
		{
			if (isset($this->packages[$pn]))
			{
				foreach ($this->packages[$pn]->version_hints as $v => $hints)
				{
					$obsoletes = [];
					if (isset($hints['obsoletes']))
						$obsoletes = $hints['obsoletes'];

					$this->add_needed_obsoletes($val, $pn, $v, $obsoletes);
				}
			}

			/* If package A is obsoleted by package B, B should appear in the */
			/* requires: for A (so the upgrade occurs with pre-depends: aware */
			/* versions of setup), but not in the depends: for A (as that creates an */
			/* unsatisfiable dependency when explicitly installing A with lisolv */
			/* versions of setup, which should just install B).  This condition can */
			/* occur since we might have synthesized the depends: from the requires: */
			/* in read_hints(), so fix that up here. */
		}

		foreach ($this->packages as $pn => $p)
		{
			foreach ($p->version_hints as $v => $hints)
			{
				if (isset($hints['obsoletes']))
				{
					foreach ($hints['obsoletes'] as $o => $constraint)
					{
						if (isset($this->packages[$o]))
						{
							$this->packages[$o]->obsolete = true;
							foreach ($this->packages[$o]->version_hints as $ov => $ohints)
							{
								if (isset($ohints['depends']))
								{
									if (isset($ohints['depends'][$pn]))
									{
										unset($this->packages[$o]->version_hints[$ov]['depends'][$pn]);
										mksetup::debug("removed '$pn' from the depends: of obsolete package '$o' '$ov'");
									}
								}
							}
						} else
						{
							mksetup::debug("can't ensure obsolete package '$o' doesn't depends: on '$pn'");
						}
					}
				}
			}

			$has_nonempty_install = false;
			if ($p->kind === PkgKind::binary)
			{
				foreach ($p->versions() as $vr)
				{
					if (!$vr->is_empty)
						$has_nonempty_install = true;
				}
			}
			$obsolete = false;
			foreach ($p->version_hints as $vr)
			{
				if (isset($vr['category']['_obsolete']))
					$obsolete = true;
			}

			/* if the package has no non-empty install tarfiles, and no dependencies */
			/* installing it will do nothing (and making it appear in the package */
			/* list is just confusing), so if it's not obsolete, mark it as */
			/* 'not_for_output' */
			if ($p->kind === PkgKind::binary)
			{
				if (!$has_nonempty_install && !$p->has_requires && !$obsolete)
				{
					if (!$p->not_for_output)
					{
						$p->not_for_output = true;
						mksetup::verbose("package '$pn' has no non-empty install tarfiles and no dependencies, marking as 'not for output'");
					}
				} else
				{
					$p->not_for_output = false;
				}
			}

			/* identify a 'best' version to take certain information from: this is */
			/* the curr version, if we have one, otherwise, the highest version. */
			$sorted_versions = $p->versions();
			uasort($sorted_versions, "Tar::reverse_compare");
			$p->best_version = null;
			foreach ($sorted_versions as $v => $tar)
			{
				if (!isset($p->version_hints[$v]['test']))
				{
					$p->best_version = $v;
					break;
				}
			}
			if ($p->best_version === null)
			{
				if (!empty($sorted_versions))
				{
					$p->best_version = array_key_first($sorted_versions);

					/* warn if no non-test ('curr') version exists */
					if (!isset($p->version_hints[$p->best_version]['disable-check']['missing-curr']) &&
						!isset($opt['disable-check']['missing-curr']))
						mksetup::error_log("warning: package '$pn' doesn't have any non-test versions (i.e. no curr: version)");
				} else
				{
					/* the package must have some versions */
					mksetup::error_log("package '$pn' doesn't have any versions");
					$p->best_version = null;
					$status = false;
				}
			}

			/* error if the curr: version isn't the most recent non-test: version */
			$mtimes = [];
			foreach ($p->versions() as $vr => $tar)
				$mtimes[$vr] = $tar->mtime;

			$cv = null;
			$nontest_versions = [];
			foreach ($sorted_versions as $v => $tar)
				if (!isset($p->version_hints[$v]['test']))
					$nontest_versions[] = $v;
			if (!empty($nontest_versions))
				$cv = $nontest_versions[0];
			arsort($mtimes, SORT_NUMERIC);
			foreach ($mtimes as $v => $mtime)
			{
				if (isset($p->version_hints[$v]) && isset($p->version_hints[$v]['test']))
					continue;
				if ($cv === null)
					continue;
				if ($cv !== $v)
				{
					if ($mtimes[$v] === $mtimes[$cv])
						/* don't consider an equal mtime to be more recent */
						continue;

					if (isset(past_mistakes::$mtime_anomalies[$pn]) ||
						isset($p->override_hints['disable-check']['curr-most-recent']) ||
						isset($opt['disable-check']['curr-most-recent']))
					{
						mksetup::debug("package '$pn' ordering discrepancy in non-test versions: '$v' has most recent timestamp, but version '$cv' is greatest");
					} else
					{
						mksetup::error_log("package '$pn' ordering discrepancy in non-test versions: '$v' has most recent timestamp, but version '$cv' is greatest");
						$status = false;
					}
				}
				break;
			}

			if ($p->override_hints !== null && isset($p->override_hints['replace-versions']))
			{
				foreach ($p->override_hints['replace-versions'] as $rv)
				{
					/* warn if replace-versions lists a version which is less than */
					/* the current version (which is pointless as the current version */
					/* will replace it anyhow) */
					$bv = $p->best_version;
					if ($bv !== null)
					{
						$a = new SetupVersion($rv);
						$b = new SetupVersion($bv);
						if (SetupVersion::compare($a, $b) <= 0)
							mksetup::error_long("warning: package '$pn' replace-versions: useless lists version '$v', which is <= current version '$bv'");
					}

					/* warn if replace-versions lists a version which is also */
					/* available to install (as this doesn't work as expected) */
					if (isset($p->version_hints[$rv]) && isset($p->version_hints[$bv]))
						if (isset($p->version_hints[$rv]['test']) === isset($p->version_hints[$bv]['test']))
							mksetup::error_log("warning: package '$pn' replace-versions: lists version '$rv', which is also available to install");
				}
			}

			/* If the install tarball is empty, we should probably either be marked */
			/* obsolete (if we have no dependencies) or virtual (if we do) */
			if ($p->kind === PkgKind::binary && !$p->not_for_output)
			{
			}
			/* If the source tarball is empty, that can't be right! */
			else if ($p->kind === PkgKind::source)
			{
				foreach ($p->versions() as $vr => $tar)
				{
					if ($tar->is_empty)
					{
						if (!isset(past_mistakes::$empty_source[$pn]) &&
							!isset($p->version_hints[$vr]['_obsolete']))
							mksetup::error_log("package '$pn' version '$vr' has empty source tar file");
					}
				}
			}
		}

		/* build inverted relations: */
		/* the set of packages which depends: on this package (rdepends), */
		/* the set of packages which build-depends: on it (build_rdepends), and */
		/* the set of packages which obsoletes: it (obsoleted_by) */
		foreach ($this->packages as $pn => $p)
		{
			foreach ($p->version_hints as $v => $hints)
			{
				foreach ([
					['depends', 'rdepends'],
					['build-depends', 'build_rdepends'],
					['obsoletes', 'obsoleted_by'],
				] as list($k, $a))
				{
					if (isset($hints[$k]))
					{
						foreach ($hints[$k] as $dp => $constraint)
						{
							if (isset($this->packages[$dp]))
								$this->packages[$dp]->$a[$pn] = $p;
						}
					}
				}
			}
		}

		/* warn about multiple obsoletes of same package */
		foreach ($this->packages as $pn => $p)
			if (count($p->obsoleted_by) >= 2)
				mksetup::debug("package '$pn' is obsoleted by more than one package: " . join(',', array_keys($p->obsoleted_by)));

		/* make another pass to verify a source tarfile exists for every install */
		/* tarfile version */
		foreach ($this->packages as $pn => $p)
		{
			if ($p->kind !== PkgKind::binary)
				continue;

			$sorted_versions = $p->versions();
			uasort($sorted_versions, "Tar::reverse_compare");
			foreach ($sorted_versions as $v => $tar)
			{
				$sourceless = false;
				$missing_source = true;

				$es_p = $p->srcpackage($v);

				/* mark the source tarfile as being used by an install tarfile */
				if (isset($this->packages[$es_p]))
				{
					if (($es_tar = $this->packages[$es_p]->tar($v)) !== null)
					{
						$es_tar->is_used = true;
						$this->packages[$es_p]->is_used_by[$pn] = $p;
						$missing_source = false;
						/*
						 * also check that they match in presence or absence test: label
						 *
						 * (this is needed if we are going to compare best_version
						 * between install and source packages for some information,
						 * as we do in some places...)
						 */
						if (isset($p->version_hints[$v]['test']) !== isset($this->packages[$es_p]->version_hints[$v]['test']))
							mksetup::error_log("package '$ün' version '$v' test: label mismatches source package '$es_p'");
					}
				}

				if ($missing_source)
				{
					/* unless the install tarfile is empty */
					if ($tar->is_empty)
					{
						$sourceless = true;
						$missing_source = false;
					}

					/* unless this package is marked as 'self-source' */
					if (isset(past_mistakes::$self_source[$pn]))
					{
						$sourceless = true;
						$missing_source = false;
					}
				}

				/* ... it's an error for this package to be missing source */
				$tar->sourceless = $sourceless;
				if ($missing_source)
				{
					mksetup::error_log("package '$pn' version '$v' is missing source");
					$status = false;
				}
			}
		}

		/* make another pass to verify that each non-empty source tarfile version has */
		/* at least one corresponding non-empty install tarfile, in some package. */
		foreach ($this->packages as $pn => $p)
		{
			$sorted_versions = $p->versions();
			uasort($sorted_versions, "Tar::reverse_compare");
			foreach ($sorted_versions as $v => $tar)
			{
				if ($p->kind !== PkgKind::source)
					continue;

				if ($tar->is_empty)
					continue;

				if (isset($p->version_hints[$v]['category']['_obsolete']))
					continue;

				if (!$tar->is_used)
				{
					mksetup::error_log("package '$pn' version '$v' source has no non-empty install tarfiles");
					$status = false;
				}
			}
		}

		/* do all the packages which use this source package have the same */
		/* current version? */
		foreach ($this->packages as $source_p)
		{
			$versions = [];

			foreach ($source_p->is_used_by as $pn => $install_p)
			{
				/* ignore packages which are getting removed */
				if (!isset($this->packages[$pn]))
					continue;

				/* ignore obsolete packages */
				if ($install_p->obsolete)
					continue;
				$obsolete = false;
				foreach ($install_p->version_hints as $vr)
				{
					if (isset($vr['category']['_obsolete']))
						$obsolete = true;
				}
				if ($obsolete)
					continue;

				/* ignore runtime library packages, as we may keep old versions of those */
				if (preg_match('/^(lib|girepository-).*[\d_.]+$|^libflint$/', $pn))
					continue;

				/* ignore Python module packages, as we may keep old versions of those */
				if (preg_match('/^python[23][5678]?-.*/', $pn))
					continue;

				/* ignore packages where best_version is a test version (i.e doesn't */
				/* have a current version, is test only), since the check we are */
				/* doing here is 'same current version' */
				if (!isset($install_p->version_hints[$install_p->best_version]['test']))
					continue;

				/* ignore packages which have a different external-source: */
				/* (e.g. where a different source package supersedes this one) */
				$es = $install_p->srcpackage($install_p->best_version);
				if ($es !== $source_p->name)
					continue;

				if (!isset(past_mistakes::$nonunique_versions[$pn]) ||
					isset($install_p->version_hints[$install_p->best_version]['disable-check']['unique-version']))
					continue;

				$versions[$install_p->best_version][$pn] = $install_p;
			}

			if (count($versions) > 1)
			{
				$out = [];
				$most_common = true;
				$sorted_versions = $versions;
				// uasort($sorted_versions, "Tar::reverse_compare");
				foreach ($sorted_versions as $vn => $v)
				{
					if ($most_common && count($v) !== 1)
						$out[] = "$vn (" . count($v) . " others)";
					else
						$out[] = "$vn (" . join(',', $v);
					$most_common = false;
				}
				$status = false;
				rsort($out);
				mksetup::error_log("install packages from source package '{$source_p->orig_name}' have non-unique current versions " . join(', ', $out));
			}
		}

		/* validate that all packages are in the package maintainers list */
		if (!$this->validate_package_maintainers($opt))
			$status = false;

		return $status;
	}


	private function add_needed_obsoletes(array $needed, string $pn, string $v, array &$obsoletes)
	{
		foreach ($needed as $n)
		{
			if (!isset($obsoletes[$n]))
			{
				$obsoletes[$n] = true;
				$this->packages[$pn]->version_hints[$v]['obsoletes'][$n] = $n;
				mksetup::verbose("added 'obsoletes: $n' to package '$pn' version '$v'");
			}

			# /* recurse so we don't drop transitive missing obsoletes */
			# if (isset($needed[$n]))
			# {
			#	mksetup::debug("recursing to examine obsoletions of '$n' for adding to '$pn'");
			#	$this->add_needed_obsoletes($needed, $pn, $v, $obsoletes);
			# }
		}
	}


	/*
	 * validate that all packages are in the package maintainers list
	 */
	private function validate_package_maintainers(array $opt): bool
	{
		$status = true;

		if (!isset($opt['pkglist']))
			return $status;

		return $status;
	}

	/*
	 * write setup.ini
	 */
	public function write_setup_ini(array $opt) : bool
	{
		if (strpos($opt['inifile'], DIR_SEP) !== false)
			$inifile = $opt['inifile'];
		else
			$inifile = $this->releasearea . DIR_SEP . $this->arch . DIR_SEP . $opt['inifile'];

		mksetup::verbose("writing $inifile");
		if (($f = fopen($inifile, "wb")) === false)
		{
			mksetup::error_log(error_get_last()['message']);
			return false;
		}

		// $t = time();
		// $tz = localtime(null, true);
		// $zone = new DateTimeZone(date_default_timezone_get());
		// $dt = new DateTime("now", $zone);
		// $offset = $zone->getOffset($dt);
		// $tz = sprintf("%04d-%02d-%02d %02d:%02d:%02d %+03d%02d", $tz['tm_year'] + 1900, $tz['tm_mon'] + 1, $tz['tm_mday'], $tz['tm_hour'], $tz['tm_min'], $tz['tm_sec'], $offset / 3600, ($offset % 3600) / 60);
		$dt = new DateTime("now");
		$tz = $dt->format("Y-m-d H:i:s O");
		$t = $dt->getTimeStamp();

		fputs($f, "# This file was automatically generated at $tz.
#
# If you edit it, your edits will be discarded next time the file is
# generated.
#
# See https://sourceware.org/cygwin-apps/setup.ini.html for a description
# of the format.
");

		if (isset($opt['release']))
			fputs($f, "release: {$opt['release']}\n");
		fputs($f, "arch: {$this->arch}\n");
		fputs($f, "setup-timestamp: $t\n");
		/* this token exists in the lexer, but not in the grammar up until */
		/* 2.878 (when it was removed), so will cause a parse error with */
		/* versions prior to that. */
		fputs($f, "include-setup: setup <2.878 not supported\n");

		/* not implemented until 2.890, ignored by earlier versions */
		fputs($f, "setup-minimum-version: 2.903\n");

		/* for setup to check if a setup upgrade is possible */
		fputs($f, "setup-version: {$opt['setup-version']}\n");

		/* a sorting which forces packages which begin with '!' to be sorted first, */
		/* packages which begin with '_" to be sorted last, and others to be sorted */
		/* case-insensitively */
		function sort_key(string $k): string
		{
			$k = strtolower($k);
			if ($k[0] === '!')
				$k = chr(0) . $k;
			else if ($k[0] === '_')
				$k = chr(255) + $k;
			return $k;
		}

		function sort_names(string $a, string $b)
		{
			return strcmp(sort_key($a), sort_key($b));
		}

		uksort($this->packages, "sort_names");

		/* helper function to output details for a particular tar file */
		function tar_line(/* resource */ $f, Package $p, string $category, string $v): void
		{
			$to = $p->tar($v);
			$fn = $to->repopath->abspath();
			fputs($f, "$category: $fn {$to->size} {$to->sha512}\n");
		}

		/* helper function to change the first character of a string to upper case, */
		/* without altering the rest */
		function upper_first_character(string $s): string
		{
			return strtoupper(substr($s, 0, 1)) . substr($s, 1);
		}

		/* for each package */
		foreach ($this->packages as $pn => $po)
		{
			if ($po->kind === PkgKind::source)
				continue;

			/* do nothing if not_for_output */
			if ($po->not_for_output)
				continue;

			/* write package data */
			fputs($f, "\n@ $pn\n");

			$bv = $po->best_version;
			if (isset($po->version_hints[$bv]['sdesc']))
				fputs($f, "sdesc: {$po->version_hints[$bv]['sdesc']}\n");
			if (isset($po->version_hints[$bv]['ldesc']))
				fputs($f, "ldesc: {$po->version_hints[$bv]['ldesc']}\n");

			$category = '';
			if (isset($po->version_hints[$bv]['category']))
				$category = join(' ', $po->version_hints[$bv]['category']);
			if ($po->orphaned)
				$category .= ' unmaintained';

			/* for historical reasons, category names must start with a capital letter */
			$category = join(' ', array_map("upper_first_character", preg_split('/[\s]/', $category, 0, PREG_SPLIT_NO_EMPTY)));
			fputs($f, "category: $category\n");

			if (isset($po->version_hints[$bv]['message']))
				fputs($f, "message: {$po->version_hints[$bv]['message']}\n");

			if (isset($po->override_hints['replace-versions']))
				fputs($f, "replace-versions: " . join(' ', $po->override_hints['replace-versions']) . "\n");

			/*
			 * make a list of version sections
			 *
			 * (they are put in a particular order to ensure certain behaviour from setup)
			 */
			$vs = [];

			/*
			 * put 'curr' first
			 *
			 * due to a historic bug in setup (fixed in 78e4c7d7), we keep the
			 * [curr] version first, to ensure that dependencies are used correctly.
			 */
			$curr_version = null;
			$nontest_versions = [];
			$sorted_versions = $po->versions();
			uasort($sorted_versions, "Tar::reverse_compare");
			foreach ($sorted_versions as $v => $tar)
				if (!isset($po->version_hints[$v]['test']))
					$nontest_versions[] = $v;
			if (!empty($nontest_versions))
			{
				$curr_version = $nontest_versions[0];
				$vs[] = [$curr_version, 'curr'];
			}

			/*
			 * purely for compatibility with previous ordering, identify the
			 * 'prev' version (the non-test version before the current version),
			 * if it exists, so we can put it last.
			 */
			$prev_version = null;
			if (count($nontest_versions) >= 2)
				$prev_version = $nontest_versions[1];

			/* ditto the 'test' version */
			$test_version = null;
			$test_versions = [];
			foreach ($sorted_versions as $v => $tar)
				if (isset($po->version_hints[$v]['test']))
					$test_versions[] = $v;
			if (!empty($test_versions))
				$test_version = $test_versions[0];

			/*
			 * next put any other versions
			 *
			 * these [prev] or [test] sections are superseded by the final ones.
			 *
			 * (to maintain historical behaviour, include versions which only
			 * exist as a source package)
			 */
			$versions = $po->versions();
			$sibling_src = $pn . '-src';
			if (isset($this->packages[$sibling_src]))
				array_update($versions, $this->packages[$sibling_src]->versions());
			$sorted_sibling_versions = $versions;
			uasort($sorted_sibling_versions, "Tar::reverse_compare");

			foreach ($sorted_sibling_versions as $version => $tar)
			{
				/* skip over versions which have a special place in the ordering: */
				/* 'curr' has already been done, 'prev' and 'test' will be done */
				/* later */
				if ($version === $curr_version || $version === $prev_version ||
					$version === $test_version)
					continue;

				/* test versions receive the test label */
				if (isset($po->version_hints[$version]['test']))
					$level = "test";
				else
					$level = "prev";
				$vs[] = [$version, $level];
			}

			/* add the 'prev' version */
			if ($prev_version !== null)
				$vs[] = [$prev_version, "prev"];

			/*
			 * finally, add the 'test' version
			 *
			 * because setup processes version sections in order, these supersede
			 * any previous [prev] and [test] sections (hopefully).  i.e. the
			 * version in the final [test] section is the one selected when test
			 * packages are requested.
			 */
			if ($test_version !== null)
				$vs[] = [$test_version, "test"];

			/* write the section for each version */
			foreach ($vs as list($version, $tag))
			{
				/* [curr] can be omitted if it's the first section */
				if ($tag !== 'curr')
					fputs($f, "[$tag]\n");
				fputs($f, "version: $version\n");

				$is_empty = false;
				if (isset($sorted_versions[$version]))
				{
					tar_line($f, $po, 'install', $version);
					$is_empty = $po->tar($version)->is_empty;
				}

				$hints = [];
				if (isset($po->version_hints[$version]))
					$hints = $po->version_hints[$version];

				/* follow external-source */
				$s = $po->srcpackage($version);
				if (!isset($this->packages[$s]))
					$s = null;

				/* external-source points to a source file in another package */
				if ($s !== null)
				{
					if (isset($this->packages[$s]) && isset($this->packages[$s]->versions()[$version]))
						tar_line($f, $this->packages[$s], 'source', $version);
					else if (!($is_empty || isset(past_mistakes::$self_source[$this->packages[$s]->orig_name])))
						mksetup::error_log("warning: package '$pn' version '$version' has no source in '{$this->packages[$s]->orig_name}'");
				}

				/* external-source should also be capable of pointing to a 'real' */
				/* source package (if cygport could generate such a thing), in */
				/* which case we should emit a 'Source:' line, and the package is */
				/* also itself emitted. */
				if (isset($sorted_versions[$version]))
				{
					if (isset($hints['depends']) && !empty($hints['depends']))
						fputs($f, "depends2: " . join(', ', $hints['depends']) . "\n");

					if (isset($hints['obsoletes']) && !empty($hints['obsoletes']))
						fputs($f, "obsoletes: " . join(', ', $hints['obsoletes']) . "\n");

					if (isset($hints['provides']) && !empty($hints['provides']))
						fputs($f, "provides: " . join(', ', $hints['provides']) . "\n");

					if (isset($hints['conflicts']) && !empty($hints['conflicts']))
						fputs($f, "conflicts: " . join(', ', $hints['conflicts']) . "\n");
				}

				if ($s !== null)
				{
					$src_hints = [];
					if (isset($this->packages[$s]->version_hints[$version]))
						$src_hints = $this->packages[$s]->version_hints[$version];
					if (isset($src_hints['build-depends']))
					{
						/* Ideally, we'd transform dependency atoms which aren't */
						/* cygwin package names into package names. For the moment, */
						/* we don't have the information to do that, so filter them */
						/* all out. */
						$bd = $src_hints['build-depends'];
						$bds = [];
						foreach ($bd as $atom => $constraint)
						{
							if (strpos($constraint, '(') === false)
								$bds[] = $atom;
						}
						if (!empty($bds))
							fprintf($f, "build-depends: %s\n", join(', ', $bds));
					}
				}
			}
		}

		fclose($f);

		return true;
	}
}


class mksetup {
	public static $opt = null;
	public static $eol;
	public static $html;

	private static $_is_cli = -1;

	/*
	 * Constructor
	 */
	public static function init(array $opt)
	{
		self::$opt = $opt;
		self::$eol = "\n";
		self::$html = $opt['html'] || !self::is_cli();

		if (self::$html)
		{
			self::$eol = "<br />\n";
			echo("<pre>\n");
		}
	}

	/*
	 * Destructor
	 */
	public function __destruct()
	{
	}


	public static function program() : string
	{
		// if (substr(php_sapi_name(), 0, 3) === 'cli') return $_SERVER["argv"][0];
		return "mksetupini";
	}


	public static function is_cli() : bool
	{
		if (self::$_is_cli < 0)
		{
			self::$_is_cli = substr(php_sapi_name(), 0, 3) === 'cli';
		}
		return self::$_is_cli;
	}


	public static function error_log(string $msg) : void
	{
		$program = self::program();
		error_log("$program: $msg");
		if (!self::is_cli())
			echo("$msg\n");
	}

	public static function quote(string $str) : string
	{
		if (!self::$html)
			return $str;
		return str_replace(' ', '&nbsp;', htmlentities($str, ENT_QUOTES));
	}


	public static function verbose(string $msg) : void
	{
		if (self::$opt['verbose'])
		{
			if (self::is_cli())
				fprintf(STDERR, "%s\n", $msg);
			else
				printf("%s{self::$eol}", self::quote($msg));
		}
	}


	public static function debug(string $msg) : void
	{
		if (self::$opt['debug'])
		{
			if (self::is_cli())
				fprintf(STDERR, "%s\n", $msg);
			else
				printf("%s{self::$eol}", self::quote($msg));
		}
	}
}


class main {
	private $packages;

	private $opt = array(
		'verbose' => false,
		'debug' => false,
		'help' => false,
		'arch' => 'x86_64',
		'disable-check' => array(),
		'inifile' => 'setup.ini',
		'pkglist' => '/www/sourceware/htdocs/cygwin/cygwin-pkg-maint',
		'release' => 'freemint',
		'releasearea' => '.',
		'spell' => false,
		'stats' => false,
		'setup-version' => '2.924',
		'html' => false,
	);

	public function __construct()
	{
		if (mksetup::is_cli())
		{
			ini_set("log_errors", 0);
			ini_set("display_errors", 1);
			error_reporting(E_ALL | E_STRICT);
		} else
		{
			ini_set("log_errors", 0);
			ini_set("display_errors", 1); /* set to 0 for production */
			error_reporting(E_ALL | E_STRICT);
		}
	}

	public function __destruct()
	{
		unset($this->opt);
		unset($this->fs);
	}

	private function usage() : void
	{
		header("Content-Type: text/plain");
		echo('
usage: ' . mksetup::program() . ' [<options>] <releasedir>

options:
  -A, --arch <arch>              architecture to use
  -d, --disable-check <checks>   checks to disable
  -u, --inifile <file>           output filename
  -p, --pkglist <file>           package maintainer list
  -r, --release <name>           value for setup-release key (default: ' . $this->opt['release'] . ')
  -a, --releasearea <dir>        release directory (default: ' . $this->opt['releasearea'] . ')
  -s, --spell                    spellcheck text hints
  -S, --stats                    show additional package statistics
  -V, --setup-version            value for setup-version key
  -v, --verbose                  print progress messages
  -h, --help                     display this helpscreen and exit
');
	}


	private function usage_error(string $msg) : void
	{
		mksetup::error_log($msg);
		if (mksetup::is_cli())
			exit(1);
	}


	private function parse_args() : void
	{
		$longopts = array(
			"verbose",
			"help",
			"arch:",
			"disable-check:",
			"inifile:",
			"pkglist:",
			"release:",
			"releasearea:",
			"spell",
			"stats",
			"setup-version:",
		);
		$options = "A:d:r:a:u:sSV:vDh";

		if (mksetup::is_cli())
		{
			$rest = 0;
			$opts = getopt($options, $longopts, $rest);
			$shortopts = preg_split('/([a-z0-9][:]{0,2})/i', $options, 0, PREG_SPLIT_DELIM_CAPTURE | PREG_SPLIT_NO_EMPTY);
			$args = array_slice($_SERVER["argv"], $rest);

			$longopts = array_merge($shortopts, $longopts);
		} else
		{
			$opts = $_GET;
		}
		foreach ($longopts as $opt)
		{
			$key = str_replace(":", "", $opt);
			$key2 = $key;
			switch ($key2)
			{
				case 'v': $key2 = 'verbose'; break;
				case 'h': $key2 = 'help'; break;
				case 'A': $key2 = 'arch'; break;
				case 'd': $key2 = 'disable-check'; break;
				case 'D': $key2 = 'debug'; break;
				case 'u': $key2 = 'inifile'; break;
				case 'p': $key2 = 'pkglist'; break;
				case 'r': $key2 = 'release'; break;
				case 'a': $key2 = 'releasearea'; break;
				case 's': $key2 = 'spell'; break;
				case 'S': $key2 = 'stats'; break;
				case 'V': $key2 = 'setup-version'; break;
			}
			if (substr($opt, -2) === '::')
			{
				if (isset($opts[$key]) && !empty($opts[$key]))
					$this->opt[$key2] = $opts[$key];
			} else if ($key2 === 'disable-check')
			{
				if (isset($opts[$key]))
				{
					if (is_array($opts[$key]))
					{
						foreach ($opts[$key] as $disable)
							foreach(explode(',', $disable) as $arg)
								if ($arg !== '')
									$this->opt[$key2][$arg] = $arg;
					} else
					{
						foreach(explode(',', $opts[$key]) as $arg)
							if ($arg !== '')
								$this->opt[$key2][$arg] = $arg;
					}
				}
			} else if (substr($opt, -1) === ':')
			{
				if (isset($opts[$key]) && !empty($opts[$key]))
					$this->opt[$key2] = $opts[$key];
			} else
			{
				if (isset($opts[$key]))
					$this->opt[$key2] = true;
			}
		}

		/*
		 * disabling either of these checks, implies both of these are disabled
		 * (since depends: is generated from requires:, and vice versa, if not
		 * present)
		 */
		$implied = array('missing-depended-package', 'missing-required-package');
		foreach ($implied as $p)
		{
			if (isset($this->opt['disable-check'][$p]))
			{
				foreach ($implied as $c)
				{
					if (!isset($this->opt['disable-check'][$c]))
						$this->opt['disable-check'][$c] = $c;
				}
			}
		}

		if (mksetup::is_cli() && isset($args[0]))
		{
			$this->opt['releasearea'] = $args[0];;
			array_shift($args);
		}
	}


	private function do_main() : bool
	{
		$status = true;

		if (!isset($this->opt['releasearea']))
		{
			mksetup::error_log("no release directory given");
			return false;
		}
		if ($this->opt['releasearea'] === '' || $this->opt['releasearea'] === '/')
		{
			mksetup::error_log("not working on root directory");
			return false;
		}
		if (!isset($this->opt['arch']))
		{
			mksetup::error_log("missing architecture");
			return false;
		}
		$this->packages = new packages($this->opt['releasearea'], $this->opt['arch']);

		if (!$this->packages->read_packages())
		{
			mksetup::error_log("errors reading package set, not writing setup.ini");
			return false;
		}

		/* spellcheck text hints */
		if ($this->opt['spell'])
		{
			mksetup::error_log("spell-checking support not available");
		}

		/* validate the package set */
		if (!$this->packages->validate($this->opt))
		{
			mksetup::error_log("package set has errors, not writing setup.ini");
			return false;
		}

		$status = $this->packages->write_setup_ini($this->opt);

		return $status;
	}


	private function do_stats() : bool
	{
		$status = true;
		$histogram = [];

		foreach ($this->packages as $p)
		{
			if (isset($p->hints['category']))
			{
				foreach ($p->hints['category'] as $c)
				{
					$c = strtolower($c);
					if (!isset($histogram[$c]))
						$histogram[$c] = 0;
					$histogram[$c] += 1;
				}
			}
		}
		arsort($histogram, SORT_NUMERIC);
		foreach ($histogram as $c => $v)
			printf("%16s: %4d\n", $c, $v);

		return $status;
	}


	public function run() : bool
	{
		$status = true;

		$this->parse_args();

		if ($this->opt['help'] !== false)
		{
			$this->usage();
		} else
		{
			try {
				mksetup::init($this->opt);
			} catch (Exception $e) {
				mksetup::error_log($e->getLine() . ": " . $e->getMessage());
				$status = false;
			}

			if ($status)
				$status = $this->do_main();
			if ($status && $this->opt['stats'])
				$status = $this->do_stats();
		}

		if (mksetup::is_cli())
			exit($status ? 0 : 1);
		return $status;
	}
}

{
	(new main())->run();
}

?>

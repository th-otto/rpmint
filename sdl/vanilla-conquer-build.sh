#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=vanilla-conquer
VERSION=
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/vanilla-conquer/0001-Implement-window-focus-events-with-SDL-1.2.patch
patches/vanilla-conquer/0002-Implement-Toggle_Video_Fullscreen-with-SDL-1.2.patch
patches/vanilla-conquer/0005-Fix-compilation-of-the-editors-when-using-SDL1.patch
patches/vanilla-conquer/0006-Use-windowed-mode-by-default-on-MiNT.patch
patches/vanilla-conquer/0007-Avoid-use-of-ftime-and-fix-overflow-of-unsigned-int.patch
patches/vanilla-conquer/0008-Avoid-conflicing-redefinitions-of-strupr-strrev.patch
patches/vanilla-conquer/0010-Avoid-concatenating-empty-paths.patch
patches/vanilla-conquer/0011-Define-_GNU_SOURCE-to-get-a-definition-of-FNM_CASEFO.patch
patches/vanilla-conquer/0012-Fix-linking-of-SDL-for-MiNT.patch
patches/vanilla-conquer/0013-Make-sure-mouse-cursor-is-not-left-disabled-when-exi.patch
patches/vanilla-conquer/0015-broadcast-addr-can-be-NULL.patch
patches/vanilla-conquer/0016-Ready_To_Quit-is-only-handled-in-WIN32-message-handl.patch
patches/vanilla-conquer/0017-Disable-useless-debug-info.patch
patches/vanilla-conquer/0018-Fix-a-narrowing-conversion.patch
patches/vanilla-conquer/0019-Fix-friend-declarations-declares-a-non-template-func.patch
patches/vanilla-conquer/0023-Fix-TFixedHeapClass-Free-not-returning-a-value.patch
patches/vanilla-conquer/0024-FootClass-Speed-is-modified-by-Set_Speed-and-must-no.patch
patches/vanilla-conquer/0027-Fix-keyboard-handling-for-SDL1.patch
patches/vanilla-conquer/0030-Fix-some-potential-buffer-overflows.patch
patches/vanilla-conquer/0031-Split-the-OpenAL-sound-code-into-common-and-OpenAL-s.patch
patches/vanilla-conquer/0032-Cleanup-initialization-of-WWPersons-array.patch
patches/vanilla-conquer/0033-Add-check-whether-compiler-supports-fdata-sections-f.patch
patches/vanilla-conquer/0034-attribute-ms_struct-is-only-valid-for-x86.patch
patches/vanilla-conquer/0035-pragma-warning-disable-is-only-valid-for-MSVC.patch
patches/vanilla-conquer/0036-Avoid-unaligned-access-to-Shape_Type-width.patch
patches/vanilla-conquer/0037-Add-needed-linker-options-for-MiNT.patch
patches/vanilla-conquer/0038-Fix-some-warnings.patch
patches/vanilla-conquer/0040-MiNT-use-clock-for-timing-which-is-much-faster.patch
"
# already applied upstream
DISABLED_PATCHES="
patches/vanilla-conquer/0003-Make-OPENAL-optional-also-on-non-windows-platforms.patch
patches/vanilla-conquer/0004-Fix-compliation-of-some-test-programs.patch
patches/vanilla-conquer/0009-Remove-unneeded-include-of-dlfcn.h.patch
patches/vanilla-conquer/0020-Fix-a-wrong-extern-definition.patch
patches/vanilla-conquer/0021-Avoid-undefined-behaviour-when-deleting-a-void.patch
patches/vanilla-conquer/0022-Avoid-redefinition-of-__USE_POSIX199309-_POSIX_C_SOU.patch
patches/vanilla-conquer/0025-Include-endianness.h-in-files-that-need-it.patch
patches/vanilla-conquer/0026-Fix-a-printf-format-TriggerClass-Write_INI.patch
patches/vanilla-conquer/0029-Fix-warnings-arithmetic-on-NULL.patch
patches/vanilla-conquer/0028-Avoid-operator-on-bool.patch
patches/vanilla-conquer/0039-Include-endianness.h-also-in-base64.patch
"

EXTRA_DIST=""

BINFILES="
${PACKAGENAME}
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing -fno-exceptions ${ELF_CFLAGS}"
STACKSIZE="-Wl,-stack,512k -Wl,--msuper-memory ${ELF_LDFLAGS}"

GST2ASCII=`which gst2ascii 2>/dev/null`

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	rm -rf build
	mkdir build
	cd build
	
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}

    # we have to set CMAKE_CXX_FLAGS_RELEASE here,
    # otherwise cmake overrides our flags and uses
    # -O3 which will produce garbage in some cases
	cmake \
		-DCMAKE_BUILD_TYPE=Release \
		-DMAP_EDITORTD=OFF \
		-DMAP_EDITORRA=OFF \
		-DBUILD_TOOLS=ON \
		-DBUILD_TESTS=OFF \
		-DSDL2=OFF \
		-DSDL1=ON \
		-DOPENAL=OFF \
		-DCMAKE_TOOLCHAIN_FILE=/usr/share/cmake/Modules/Platform/${TARGET}.cmake \
		-DCMAKE_C_COMPILER="${TARGET}-gcc" \
		-DCMAKE_CXX_COMPILER="${TARGET}-g++" \
		-DCMAKE_CXX_FLAGS="${CPU_CFLAGS}" \
		-DCMAKE_CXX_FLAGS_DEBUG="-g -fno-strict-aliasing ${ELF_CFLAGS}" \
		-DCMAKE_CXX_FLAGS_RELEASE="${COMMON_CFLAGS}" \
		-DCMAKE_EXE_LINKER_FLAGS="${STACKSIZE}" \
		.. || exit 1

	${MAKE} $JOBS || exit 1

	mkdir -p "${THISPKG_DIR}"
	cp -p vanillatd "${THISPKG_DIR}/vanillatd-${CPU}.prg" || exit 1
	cp -p vanillara "${THISPKG_DIR}/vanillara-${CPU}.prg" || exit 1
	cp -p vanillamix "${THISPKG_DIR}/vanillamix-${CPU}.ttp" || exit 1
	if test "$GST2ASCII" != ""; then
		"$GST2ASCII" -a -b -d -l "${THISPKG_DIR}/vanillatd-${CPU}.prg" | ${TARGET}-c++filt > "${THISPKG_DIR}/vanillatd-${CPU}.sym"
		"$GST2ASCII" -a -b -d -l "${THISPKG_DIR}/vanillara-${CPU}.prg" | ${TARGET}-c++filt > "${THISPKG_DIR}/vanillara-${CPU}.sym"
		"$GST2ASCII" -a -b -d -l "${THISPKG_DIR}/vanillamix-${CPU}.ttp" | ${TARGET}-c++filt > "${THISPKG_DIR}/vanillamix-${CPU}.sym"
	fi
	${TARGET}-strip "${THISPKG_DIR}/"*.prg
	${TARGET}-strip "${THISPKG_DIR}/"*.ttp 
	cp -p vanillatd.map "${THISPKG_DIR}/vanillatd-${CPU}.map" >/dev/null || true
	cp -p vanillara.map "${THISPKG_DIR}/vanillara-${CPU}.map" >/dev/null || true
done

cd "$MINT_BUILD_DIR"

cd "${THISPKG_DIR}"

make_bin_archive
make_archives

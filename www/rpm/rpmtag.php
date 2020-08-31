<?php

/* The RPM data types that are stored in headers */
define('RPM_TYPE_NULL',         0);
define('RPM_TYPE_CHAR',         1);
define('RPM_TYPE_INT8',         2);
define('RPM_TYPE_INT16',        3);
define('RPM_TYPE_INT32',        4);
define('RPM_TYPE_INT64',        5);
define('RPM_TYPE_STRING',       6);
define('RPM_TYPE_BIN',          7);
define('RPM_TYPE_STRING_ARRAY', 8);
define('RPM_TYPE_I18NSTRING',   9);
define('RPM_TYPE_ASN1',         10); /* obsolete */
define('RPM_TYPE_OPENPGP',      11); /* obsolete */

define('RPM_ANY_RETURN_TYPE',     0);
define('RPM_SCALAR_RETURN_TYPE',  0x00010000);
define('RPM_ARRAY_RETURN_TYPE',   0x00020000);
define('RPM_MAPPING_RETURN_TYPE', 0x00040000);
define('RPM_MASK_RETURN_TYPE',    0xffff0000);


/* 
 * These constants are the tags that we are going to support in the
 * RPM file.  There may be more tags, but these are the ones we
 * will be supporting.  Most of the tags that have been removed are
 * tags which have been deprecated, obsoleted, unused, or are very
 * internal with no real use to this module
 */
define('RPMTAG_NAME',                      1000); /* s */
define('RPMTAG_VERSION',                   1001); /* s */
define('RPMTAG_RELEASE',                   1002); /* s */
define('RPMTAG_EPOCH',                     1003); /* i */
define('RPMTAG_SERIAL',                    RPMTAG_EPOCH);
define('RPMTAG_SUMMARY',                   1004); /* s{} */
define('RPMTAG_DESCRIPTION',               1005); /* s{} */
define('RPMTAG_BUILDTIME',                 1006); /* i */
define('RPMTAG_BUILDHOST',                 1007); /* s */
define('RPMTAG_INSTALLTIME',               1008); /* i */
define('RPMTAG_SIZE',                      1009); /* i */
define('RPMTAG_DISTRIBUTION',              1010); /* s */
define('RPMTAG_VENDOR',                    1011); /* s */
define('RPMTAG_GIF',                       1012); /* x */
define('RPMTAG_XPM',                       1013); /* x */
define('RPMTAG_LICENSE',                   1014); /* s */
define('RPMTAG_COPYRIGHT',                 RPMTAG_LICENSE);
define('RPMTAG_PACKAGER',                  1015); /* s */
define('RPMTAG_GROUP',                     1016); /* s{} */
define('RPMTAG_CHANGELOG',                 1017); /* s[] internal */
define('RPMTAG_SOURCE',                    1018); /* s[] */
define('RPMTAG_PATCH',                     1019); /* s[] */
define('RPMTAG_URL',                       1020); /* s */
define('RPMTAG_OS',                        1021); /* s legacy used int */
define('RPMTAG_ARCH',                      1022); /* s legacy used int */
define('RPMTAG_PREIN',                     1023); /* s */
define('RPMTAG_POSTIN',                    1024); /* s */
define('RPMTAG_PREUN',                     1025); /* s */
define('RPMTAG_POSTUN',                    1026); /* s */
define('RPMTAG_OLDFILENAMES',              1027); /* s[] obsolete */
define('RPMTAG_FILESIZES',                 1028); /* i[] */
define('RPMTAG_FILESTATES',                1029); /* c[] */
define('RPMTAG_FILEMODES',                 1030); /* h[] */
define('RPMTAG_FILEUIDS',                  1031); /* i[] internal - obsolete */
define('RPMTAG_FILEGIDS',                  1032); /* i[] internal - obsolete */
define('RPMTAG_FILERDEVS',                 1033); /* h[] */
define('RPMTAG_FILEMTIMES',                1034); /* i[] */
define('RPMTAG_FILEMD5S',                  1035); /* s[] */
define('RPMTAG_FILEDIGESTS',               RPMTAG_FILEMD5S);
define('RPMTAG_FILELINKTOS',               1036); /* s[] */
define('RPMTAG_FILEFLAGS',                 1037); /* i[] */
define('RPMTAG_ROOT',                      1038); /* internal - obsolete */
define('RPMTAG_FILEUSERNAME',              1039); /* s[] */
define('RPMTAG_FILEGROUPNAME',             1040); /* s[] */
define('RPMTAG_EXCLUDE',                   1041); /* internal - obsolete */
define('RPMTAG_EXCLUSIVE',                 1042); /* internal - obsolete */
define('RPMTAG_ICON',                      1043); /* x */
define('RPMTAG_SOURCERPM',                 1044); /* s */
define('RPMTAG_FILEVERIFYFLAGS',           1045); /* i[] */
define('RPMTAG_ARCHIVESIZE',               1046); /* i */
define('RPMTAG_PROVIDENAME',               1047); /* s[] */
define('RPMTAG_PROVIDES',                  RPMTAG_PROVIDENAME);
define('RPMTAG_REQUIREFLAGS',              1048); /* i[] */
define('RPMTAG_REQUIRENAME',               1049); /* s[] */
define('RPMTAG_REQUIRES',                  RPMTAG_REQUIRENAME); /* s[] */
define('RPMTAG_REQUIREVERSION',            1050); /* s[] */
define('RPMTAG_NOSOURCE',                  1051); /* i[] */
define('RPMTAG_NOPATCH',                   1052); /* i[] */
define('RPMTAG_CONFLICTFLAGS',             1053); /* i[] */
define('RPMTAG_CONFLICTNAME',              1054); /* s[] */
define('RPMTAG_CONFLICTS',                 RPMTAG_CONFLICTNAME); /* s[] */
define('RPMTAG_CONFLICTVERSION',           1055); /* s[] */
define('RPMTAG_DEFAULTPREFIX',             1056); /* s internal - deprecated */
define('RPMTAG_BUILDROOT',                 1057); /* s internal - obsolete */
define('RPMTAG_INSTALLPREFIX',             1058); /* s internal - deprecated */
define('RPMTAG_EXCLUDEARCH',               1059); /* s[] */
define('RPMTAG_EXCLUDEOS',                 1060); /* s[] */
define('RPMTAG_EXCLUSIVEARCH',             1061); /* s[] */
define('RPMTAG_EXCLUSIVEOS',               1062); /* s[] */
define('RPMTAG_AUTOREQPROV',               1063); /* s internal */
define('RPMTAG_RPMVERSION',                1064); /* s */
define('RPMTAG_TRIGGERSCRIPTS',            1065); /* s[] */
define('RPMTAG_TRIGGERNAME',               1066); /* s[] */
define('RPMTAG_TRIGGERVERSION',            1067); /* s[] */
define('RPMTAG_TRIGGERFLAGS',              1068); /* i[] */
define('RPMTAG_TRIGGERINDEX',              1069); /* i[] */
define('RPMTAG_VERIFYSCRIPT',              1079); /* s */
define('RPMTAG_CHANGELOGTIME',             1080); /* i[] */
define('RPMTAG_CHANGELOGNAME',             1081); /* s[] */
define('RPMTAG_CHANGELOGTEXT',             1082); /* s[] */
define('RPMTAG_BROKENMD5',                 1083); /* internal - obsolete */
define('RPMTAG_PREREQ',                    1084); /* internal */
define('RPMTAG_PREINPROG',                 1085); /* s[] */
define('RPMTAG_POSTINPROG',                1086); /* s[] */
define('RPMTAG_PREUNPROG',                 1087); /* s[] */
define('RPMTAG_POSTUNPROG',                1088); /* s[] */
define('RPMTAG_BUILDARCHS',                1089); /* s[] */
define('RPMTAG_OBSOLETENAME',              1090); /* s[] */
define('RPMTAG_OBSOLETES',                 RPMTAG_OBSOLETENAME); /* s[] */
define('RPMTAG_VERIFYSCRIPTPROG',          1091); /* s[] */
define('RPMTAG_TRIGGERSCRIPTPROG',         1092); /* s[] */
define('RPMTAG_DOCDIR',                    1093); /* internal */
define('RPMTAG_COOKIE',                    1094); /* s */
define('RPMTAG_FILEDEVICES',               1095); /* i[] */
define('RPMTAG_FILEINODES',                1096); /* i[] */
define('RPMTAG_FILELANGS',                 1097); /* s[] */
define('RPMTAG_PREFIXES',                  1098); /* s[] */
define('RPMTAG_INSTPREFIXES',              1099); /* s[] */
define('RPMTAG_TRIGGERIN',                 1100); /* internal */
define('RPMTAG_TRIGGERUN',                 1101); /* internal */
define('RPMTAG_TRIGGERPOSTUN',             1102); /* internal */
define('RPMTAG_AUTOREQ',                   1103); /* internal */
define('RPMTAG_AUTOPROV',                  1104); /* internal */
define('RPMTAG_CAPABILITY',                1105); /* i internal - obsolete */
define('RPMTAG_SOURCEPACKAGE',             1106); /* i */
define('RPMTAG_OLDORIGFILENAMES',          1107); /* internal - obsolete */
define('RPMTAG_BUILDPREREQ',               1108); /* internal */
define('RPMTAG_BUILDREQUIRES',             1109); /* internal */
define('RPMTAG_BUILDCONFLICTS',            1110); /* internal */
define('RPMTAG_BUILDMACROS',               1111); /* internal - unused */
define('RPMTAG_PROVIDEFLAGS',              1112); /* i[] */
define('RPMTAG_PROVIDEVERSION',            1113); /* s[] */
define('RPMTAG_OBSOLETEFLAGS',             1114); /* i[] */
define('RPMTAG_OBSOLETEVERSION',           1115); /* s[] */
define('RPMTAG_DIRINDEXES',                1116); /* i[] */
define('RPMTAG_BASENAMES',                 1117); /* s[] */
define('RPMTAG_DIRNAMES',                  1118); /* s[] */
define('RPMTAG_ORIGDIRINDEXES',            1119); /* i[] relocation */
define('RPMTAG_ORIGBASENAMES',             1120); /* s[] relocation */
define('RPMTAG_ORIGDIRNAMES',              1121); /* s[] relocation */
define('RPMTAG_OPTFLAGS',                  1122); /* s */
define('RPMTAG_DISTURL',                   1023); /* s */
define('RPMTAG_PAYLOADFORMAT',             1124); /* s */
define('RPMTAG_PAYLOADCOMPRESSOR',         1125); /* s */
define('RPMTAG_PAYLOADFLAGS',              1126); /* s */
define('RPMTAG_INSTALLCOLOR',              1127); /* i transaction color when installed */
define('RPMTAG_INSTALLTID',                1128); /* i */
define('RPMTAG_REMOVETID',                 1129); /* i */
define('RPMTAG_SHA1RHN',                   1130); /* internal - obsolete */
define('RPMTAG_RHNPLATFORM',               1131); /* s internal - obsolete */
define('RPMTAG_PLATFORM',                  1132); /* s */
define('RPMTAG_PATCHESNAME',               1133); /* s[] deprecated placeholder (SuSE) */
define('RPMTAG_PATCHESFLAGS',              1134); /* i[] deprecated placeholder (SuSE) */
define('RPMTAG_PATCHESVERSION',            1135); /* s[] deprecated placeholder (SuSE) */
define('RPMTAG_CACHECTIME',                1136); /* i internal - obsolete */
define('RPMTAG_CACHEPKGPATH',              1137); /* s internal - obsolete */
define('RPMTAG_CACHEPKGSIZE',              1138); /* i internal - obsolete */
define('RPMTAG_CACHEPKGMTIME',             1139); /* i internal - obsolete */
define('RPMTAG_FILECOLORS',                1140); /* i[] */
define('RPMTAG_FILECLASS',                 1141); /* i[] */
define('RPMTAG_CLASSDICT',                 1142); /* s[] */
define('RPMTAG_FILEDEPENDSX',              1143); /* i[] */
define('RPMTAG_FILEDEPENDSN',              1144); /* i[] */
define('RPMTAG_DEPENDSDICT',               1145); /* i[] */
define('RPMTAG_SOURCEPKGID',               1146); /* x */
define('RPMTAG_FILECONTEXTS',              1147); /* s[] - obsolete */
define('RPMTAG_FSCONTEXTS',                1148); /* s[] extension */
define('RPMTAG_RECONTEXTS',                1149); /* s[] extension */
define('RPMTAG_POLICIES',                  1150); /* s[] selinux *.te policy file. */
define('RPMTAG_PRETRANS',                  1151); /* s */
define('RPMTAG_POSTTRANS',                 1152); /* s */
define('RPMTAG_PRETRANSPROG',              1153); /* s[] */
define('RPMTAG_POSTTRANSPROG',             1154); /* s[] */
define('RPMTAG_DISTTAG',                   1155); /* s */
define('RPMTAG_OLDSUGGESTSNAME',           1156); /* s[] - obsolete */
define('RPMTAG_OLDSUGGESTS',               RPMTAG_OLDSUGGESTSNAME); /* s[] - obsolete */

define('RPMTAG_OLDSUGGESTSVERSION',        1157); /* s[] - obsolete */
define('RPMTAG_OLDSUGGESTSFLAGS',          1158); /* i[] - obsolete */
define('RPMTAG_OLDENHANCESNAME',           1159); /* s[] - obsolete */
define('RPMTAG_OLDENHANCES',               RPMTAG_OLDENHANCESNAME); /* s[] - obsolete */
define('RPMTAG_OLDENHANCESVERSION',        1160); /* s[] - obsolete */
define('RPMTAG_OLDENHANCESFLAGS',          1161); /* i[] - obsolete */
define('RPMTAG_PRIORITY',                  1162); /* i[] extension placeholder (unimplemented) */
define('RPMTAG_CVSID',                     1163); /* s (unimplemented) */
define('RPMTAG_SVNID',                     RPMTAG_CVSID); /* s (unimplemented) */
define('RPMTAG_BLINKPKGID',                1164); /* s[] (unimplemented) */
define('RPMTAG_BLINKHDRID',                1165); /* s[] (unimplemented) */
define('RPMTAG_BLINKNEVRA',                1166); /* s[] (unimplemented) */
define('RPMTAG_FLINKPKGID',                1167); /* s[] (unimplemented) */
define('RPMTAG_FLINKHDRID',                1168); /* s[] (unimplemented) */
define('RPMTAG_FLINKNEVRA',                1169); /* s[] (unimplemented) */
define('RPMTAG_PACKAGEORIGIN',             1170); /* s (unimplemented) */
define('RPMTAG_TRIGGERPREIN',              1171); /* internal */
define('RPMTAG_BUILDSUGGESTS',             1172); /* internal (unimplemented) */
define('RPMTAG_BUILDENHANCES',             1173); /* internal (unimplemented) */
define('RPMTAG_SCRIPTSTATES',              1174); /* i[] scriptlet exit codes (unimplemented) */
define('RPMTAG_SCRIPTMETRICS',             1175); /* i[] scriptlet execution times (unimplemented) */
define('RPMTAG_BUILDCPUCLOCK',             1176); /* i (unimplemented) */
define('RPMTAG_FILEDIGESTALGOS',           1177); /* i[] (unimplemented) */
define('RPMTAG_VARIANTS',                  1178); /* s[] (unimplemented) */
define('RPMTAG_XMAJOR',                    1179); /* i (unimplemented) */
define('RPMTAG_XMINOR',                    1180); /* i (unimplemented) */
define('RPMTAG_REPOTAG',                   1181); /* s (unimplemented) */
define('RPMTAG_KEYWORDS',                  1182); /* s[] (unimplemented) */
define('RPMTAG_BUILDPLATFORMS',            1183); /* s[] (unimplemented) */
define('RPMTAG_PACKAGECOLOR',              1184); /* i (unimplemented) */
define('RPMTAG_PACKAGEPREFCOLOR',          1185); /* i (unimplemented) */
define('RPMTAG_XATTRSDICT',                1186); /* s[] (unimplemented) */
define('RPMTAG_FILEXATTRSX',               1187); /* i[] (unimplemented) */
define('RPMTAG_DEPATTRSDICT',              1188); /* s[] (unimplemented) */
define('RPMTAG_CONFLICTATTRSX',            1189); /* i[] (unimplemented) */
define('RPMTAG_OBSOLETEATTRSX',            1190); /* i[] (unimplemented) */
define('RPMTAG_PROVIDEATTRSX',             1191); /* i[] (unimplemented) */
define('RPMTAG_REQUIREATTRSX',             1192); /* i[] (unimplemented) */
define('RPMTAG_BUILDPROVIDES',             1193); /* internal (unimplemented) */
define('RPMTAG_BUILDOBSOLETES',            1194); /* internal (unimplemented) */
define('RPMTAG_DBINSTANCE',                1195); /* i extension */
define('RPMTAG_NVRA',                      1196); /* s extension */

/* tags 1997-4999 reserved */
define('RPMTAG_FILENAMES',                 5000); /* s[] extension */
define('RPMTAG_FILEPROVIDE',               5001); /* s[] extension */
define('RPMTAG_FILEREQUIRE',               5002); /* s[] extension */
define('RPMTAG_FSNAMES',                   5003); /* s[] (unimplemented) */
define('RPMTAG_FSSIZES',                   5004); /* l[] (unimplemented) */
define('RPMTAG_TRIGGERCONDS',              5005); /* s[] extension */
define('RPMTAG_TRIGGERTYPE',               5006); /* s[] extension */
define('RPMTAG_ORIGFILENAMES',             5007); /* s[] extension */
define('RPMTAG_LONGFILESIZES',             5008); /* l[] */
define('RPMTAG_LONGSIZE',                  5009); /* l */
define('RPMTAG_FILECAPS',                  5010); /* s[] */
define('RPMTAG_FILEDIGESTALGO',            5011); /* i file digest algorithm */
define('RPMTAG_BUGURL',                    5012); /* s */
define('RPMTAG_EVR',                       5013); /* s extension */
define('RPMTAG_NVR',                       5014); /* s extension */
define('RPMTAG_NEVR',                      5015); /* s extension */
define('RPMTAG_NEVRA',                     5016); /* s extension */
define('RPMTAG_HEADERCOLOR',               5017); /* i extension */
define('RPMTAG_VERBOSE',                   5018); /* i extension */
define('RPMTAG_EPOCHNUM',                  5019); /* i extension */
define('RPMTAG_PREINFLAGS',                5020); /* i */
define('RPMTAG_POSTINFLAGS',               5021); /* i */
define('RPMTAG_PREUNFLAGS',                5022); /* i */
define('RPMTAG_POSTUNFLAGS',               5023); /* i */
define('RPMTAG_PRETRANSFLAGS',             5024); /* i */
define('RPMTAG_POSTTRANSFLAGS',            5025); /* i */
define('RPMTAG_VERIFYSCRIPTFLAGS',         5026); /* i */
define('RPMTAG_TRIGGERSCRIPTFLAGS',        5027); /* i[] */
define('RPMTAG_COLLECTIONS',               5029); /* s[] list of collections (unimplemented) */
define('RPMTAG_POLICYNAMES',               5030); /* s[] */
define('RPMTAG_POLICYTYPES',               5031); /* s[] */
define('RPMTAG_POLICYTYPESINDEXES',        5032); /* i[] */
define('RPMTAG_POLICYFLAGS',               5033); /* i[] */
define('RPMTAG_VCS',                       5034); /* s */
define('RPMTAG_ORDERNAME',                 5035); /* s[] */
define('RPMTAG_ORDERVERSION',              5036); /* s[] */
define('RPMTAG_ORDERFLAGS',                5037); /* i[] */
define('RPMTAG_MSSFMANIFEST',              5038); /* s[] reservation (unimplemented) */
define('RPMTAG_MSSFDOMAIN',                5039); /* s[] reservation (unimplemented) */
define('RPMTAG_INSTFILENAMES',             5040); /* s[] extension */
define('RPMTAG_REQUIRENEVRS',              5041); /* s[] extension */
define('RPMTAG_PROVIDENEVRS',              5042); /* s[] extension */
define('RPMTAG_OBSOLETENEVRS',             5043); /* s[] extension */
define('RPMTAG_CONFLICTNEVRS',             5044); /* s[] extension */
define('RPMTAG_FILENLINKS',                5045); /* i[] extension */
define('RPMTAG_RECOMMENDNAME',             5046); /* s[] */
define('RPMTAG_RECOMMENDS',                RPMTAG_RECOMMENDNAME); /* s[] */
define('RPMTAG_RECOMMENDVERSION',          5047); /* s[] */
define('RPMTAG_RECOMMENDFLAGS',            5048); /* i[] */
define('RPMTAG_SUGGESTNAME',               5049); /* s[] */
define('RPMTAG_SUGGESTS',                  RPMTAG_SUGGESTNAME); /* s[] */
define('RPMTAG_SUGGESTVERSION',            5050); /* s[] extension */
define('RPMTAG_SUGGESTFLAGS',              5051); /* i[] extension */
define('RPMTAG_SUPPLEMENTNAME',            5052); /* s[] */
define('RPMTAG_SUPPLEMENTS',               RPMTAG_SUPPLEMENTNAME); /* s[] */
define('RPMTAG_SUPPLEMENTVERSION',         5053); /* s[] */
define('RPMTAG_SUPPLEMENTFLAGS',           5054); /* i[] */
define('RPMTAG_ENHANCENAME',               5055); /* s[] */
define('RPMTAG_ENHANCES',                  RPMTAG_ENHANCENAME); /* s[] */
define('RPMTAG_ENHANCEVERSION',            5056); /* s[] */
define('RPMTAG_ENHANCEFLAGS',              5057); /* i[] */
define('RPMTAG_RECOMMENDNEVRS',            5058); /* s[] extension */
define('RPMTAG_SUGGESTNEVRS',              5059); /* s[] extension */
define('RPMTAG_SUPPLEMENTNEVRS',           5060); /* s[] extension */
define('RPMTAG_ENHANCENEVRS',              5061); /* s[] extension */
define('RPMTAG_ENCODING',                  5062); /* s */
define('RPMTAG_FILETRIGGERIN',             5063); /* internal */
define('RPMTAG_FILETRIGGERUN',             5064); /* internal */
define('RPMTAG_FILETRIGGERPOSTUN',         5065); /* internal */
define('RPMTAG_FILETRIGGERSCRIPTS',        5066); /* s[] */
define('RPMTAG_FILETRIGGERSCRIPTPROG',     5067); /* s[] */
define('RPMTAG_FILETRIGGERSCRIPTFLAGS',    5068); /* i[] */
define('RPMTAG_FILETRIGGERNAME',           5069); /* s[] */
define('RPMTAG_FILETRIGGERINDEX',          5070); /* i[] */
define('RPMTAG_FILETRIGGERVERSION',        5071); /* s[] */
define('RPMTAG_FILETRIGGERFLAGS',          5072); /* i[] */
define('RPMTAG_TRANSFILETRIGGERIN',        5073); /* internal */
define('RPMTAG_TRANSFILETRIGGERUN',        5074); /* internal */
define('RPMTAG_TRANSFILETRIGGERPOSTUN',    5075); /* internal */
define('RPMTAG_TRANSFILETRIGGERSCRIPTS',   5076); /* s[] */
define('RPMTAG_TRANSFILETRIGGERSCRIPTPROG',  5077); /* s[] */
define('RPMTAG_TRANSFILETRIGGERSCRIPTFLAGS', 5078); /* i[] */
define('RPMTAG_TRANSFILETRIGGERNAME',      5079); /* s[] */
define('RPMTAG_TRANSFILETRIGGERINDEX',     5080); /* i[] */
define('RPMTAG_TRANSFILETRIGGERVERSION',   5081); /* s[] */
define('RPMTAG_TRANSFILETRIGGERFLAGS',     5082); /* i[] */
define('RPMTAG_REMOVEPATHPOSTFIXES',       5083); /* s internal */
define('RPMTAG_FILETRIGGERPRIORITIES',     5084); /* i[] */
define('RPMTAG_TRANSFILETRIGGERPRIORITIES', 5085); /* i[] */
define('RPMTAG_FILETRIGGERCONDS',          5086); /* s[] extension */
define('RPMTAG_FILETRIGGERTYPE',           5087); /* s[] extension */
define('RPMTAG_TRANSFILETRIGGERCONDS',     5088); /* s[] extension */
define('RPMTAG_TRANSFILETRIGGERTYPE',      5089); /* s[] extension */
define('RPMTAG_FILESIGNATURES',            5090); /* s[] */
define('RPMTAG_FILESIGNATURELENGTH',       5091); /* i */
define('RPMTAG_PAYLOADDIGEST',             5092); /* s[] */
define('RPMTAG_PAYLOADDIGESTALGO',         5093); /* i */
define('RPMTAG_AUTOINSTALLED',             5094); /* i reservation (unimplemented) */
define('RPMTAG_IDENTITY',                  5095); /* s reservation (unimplemented) */
define('RPMTAG_MODULARITYLABEL',           5096); /* s */


/*
 * Dependency Attributes.
 */
define('RPMSENSE_ANY',           0);
define('RPMSENSE_LESS',          0x00000002);
define('RPMSENSE_GREATER',       0x00000004);
define('RPMSENSE_EQUAL',         0x00000008);
/* bit 4 unused */
define('RPMSENSE_POSTTRANS',     0x00000020); /* %posttrans dependency */
define('RPMSENSE_PREREQ',        0x00000040); /* legacy prereq dependency */
define('RPMSENSE_PRETRANS',      0x00000080); /* Pre-transaction dependency. */
define('RPMSENSE_INTERP',        0x00000100); /* Interpreter used by scriptlet. */
define('RPMSENSE_SCRIPT_PRE',    0x00000200); /* %pre dependency. */
define('RPMSENSE_SCRIPT_POST',   0x00000400); /* %post dependency. */
define('RPMSENSE_SCRIPT_PREUN',  0x00000800); /* %preun dependency. */
define('RPMSENSE_SCRIPT_POSTUN', 0x00001000); /* %postun dependency. */
define('RPMSENSE_SCRIPT_VERIFY', 0x00002000); /* %verify dependency. */
define('RPMSENSE_FIND_REQUIRES', 0x00004000); /* find-requires generated dependency. */
define('RPMSENSE_FIND_PROVIDES', 0x00008000); /* find-provides generated dependency. */

define('RPMSENSE_TRIGGERIN',     0x00010000); /* %triggerin dependency. */
define('RPMSENSE_TRIGGERUN',     0x00020000); /* %triggerun dependency. */
define('RPMSENSE_TRIGGERPOSTUN', 0x00040000); /* %triggerpostun dependency. */
define('RPMSENSE_MISSINGOK',     0x00080000); /* suggests/enhances hint. */
/* bits 20-23 unused */
define('RPMSENSE_RPMLIB',        0x01000000); /* rpmlib(feature) dependency. */
define('RPMSENSE_TRIGGERPREIN',  0x02000000); /* %triggerprein dependency. */
define('RPMSENSE_KEYRING',       0x04000000);
/* bit 27 unused */
define('RPMSENSE_CONFIG',        0x10000000);
define('RPMSENSE_SENSEMASK', 15);  /* Mask to get senses, ie serial, */

/*
 * File types.
 * These are the file types used internally by rpm. The file
 * type is determined by applying stat(2) macros like S_ISDIR to
 * the file mode tag from a header. The values are arbitrary,
 * but are identical to the linux stat(2) file types.
 */
define('RPMFILE_TYPE_PIPE', 1);  /* pipe/fifo */
define('RPMFILE_TYPE_CDEV', 2);  /* character device */
define('RPMFILE_TYPE_DIR',  4);  /* directory */
define('RPMFILE_TYPE_BDEV', 6);  /* block device */
define('RPMFILE_TYPE_REG',  8);  /* regular file */
define('RPMFILE_TYPE_LINK', 10); /* hard link */
define('RPMFILE_TYPE_SOCK', 12); /* socket */

/*
 * File States (when installed).
 */
define('RPMFILE_STATE_MISSING',     -1); /* used for unavailable data */
define('RPMFILE_STATE_NORMAL',       0);
define('RPMFILE_STATE_REPLACED',     1);
define('RPMFILE_STATE_NOTINSTALLED', 2);
define('RPMFILE_STATE_NETSHARED',    3);
define('RPMFILE_STATE_WRONGCOLOR',   4);

/*
 * Exported File Attributes (ie RPMTAG_FILEFLAGS)
 */
define('RPMFILE_NONE',      0);
define('RPMFILE_CONFIG',    0x0001);	/* from %%config */
define('RPMFILE_DOC',       0x0002);	/* from %%doc */
define('RPMFILE_ICON',      0x0004);	/* from %%donotuse. */
define('RPMFILE_MISSINGOK', 0x0008);	/* from %%config(missingok) */
define('RPMFILE_NOREPLACE', 0x0010);	/* from %%config(noreplace) */
define('RPMFILE_SPECFILE',  0x0020);	/* @todo (unnecessary) marks 1st file in srpm. */
define('RPMFILE_GHOST',     0x0040);	/* from %%ghost */
define('RPMFILE_LICENSE',   0x0080);	/* from %%license */
define('RPMFILE_README',    0x0100);	/* from %%readme */
/* bits 9-10 unused */
define('RPMFILE_PUBKEY',    0x0800);	/* from %%pubkey */
define('RPMFILE_ARTIFACT',  0x1000);	/* from %%artifact */


/*
 * Tags found in signature header from package.
 */
define('RPMTAG_HEADERIMAGE',        61);   /* Current image. */
define('RPMTAG_HEADERSIGNATURES',   62);   /* Signatures. */
define('RPMTAG_HEADERIMMUTABLE',	63);   /* s[] Original image. */
define('RPMTAG_HEADERREGIONS',      64);   /* Regions. */
define('RPMTAG_HEADERI18NTABLE',    100);  /* s[] I18N string locales. */

define('RPMTAG_SIG_BASE',           256);  /* internal Broken SHA1, take 1. */
define('RPMTAG_SIGSIZE',            257);  /* i */
define('RPMTAG_SIGLEMD5_1',         258);  /* internal - obsolete */
define('RPMTAG_SIGPGP',             259);  /* x */
define('RPMTAG_SIGLEMD5_2',         260);  /* internal - obsolete */
define('RPMTAG_SIGMD5',             261);  /* x */
define('RPMTAG_PKGID',              RPMTAG_SIGMD5);  /* x */
define('RPMTAG_SIGGPG',             262);  /* x */
define('RPMTAG_SIGPGP5',            263);  /* internal - obsolete */
define('RPMTAG_BADSHA1_1',          264);  /* internal Broken SHA1, take 1. */
define('RPMTAG_BADSHA1_2',          265);  /* internal Broken SHA1, take 2. */
define('RPMTAG_PUBKEYS',            266);  /* s[]. */
define('RPMTAG_DSAHEADER',          267);  /* internal DSA header signature. */
define('RPMTAG_RSAHEADER',          268);  /* internal RSA header signature. */
define('RPMTAG_SHA1HEADER',         269);  /* internal sha1 header digest. */
define('RPMTAG_HDRID',              RPMTAG_SHA1HEADER);  /* internal sha1 header digest. */
define('RPMTAG_LONGSIGSIZE',        270);  /* internal Header+Payload size (64bit) in bytes. */
define('RPMTAG_LONGARCHIVESIZE',    271);  /* internal uncompressed payload size (64bit) in bytes. */
define('RPMTAG_SHA256HEADER',       273);
define('RPMTAG_FILESIGNATURESHEADER', 274);
define('RPMTAG_FILESIGNATURELENGTHHEADER',275);


define('RPMSIGTAG_SIZE',            1000); /* internal Header+Payload size (32bit) in bytes. */
define('RPMSIGTAG_LEMD5_1',         1001); /* internal Broken MD5, take 1 @deprecated legacy. */
define('RPMSIGTAG_PGP',             1002); /* internal PGP 2.6.3 signature. */
define('RPMSIGTAG_LEMD5_2',         1003); /* internal Broken MD5, take 2 @deprecated legacy. */
define('RPMSIGTAG_MD5',             1004); /* internal MD5 signature. */
define('RPMSIGTAG_PKGID',           RPMSIGTAG_MD5); /* internal MD5 signature. */
define('RPMSIGTAG_GPG',             1005); /* internal GnuPG signature. */
define('RPMSIGTAG_PGP5',            1006); /* internal PGP5 signature @deprecated legacy. */
define('RPMSIGTAG_PAYLOADSIZE',     1007); /* internal uncompressed payload size (32bit) in bytes. */
define('RPMSIGTAG_RESERVEDSPACE',   1008); /* internal space reserved for signatures */
define('RPMSIGTAG_BADSHA1_1',       RPMTAG_BADSHA1_1);  /* internal Broken SHA1, take 1. */
define('RPMSIGTAG_BADSHA1_2',       RPMTAG_BADSHA1_2);  /* internal Broken SHA1, take 2. */
define('RPMSIGTAG_DSA',             RPMTAG_DSAHEADER);  /* internal DSA header signature. */
define('RPMSIGTAG_RSA',             RPMTAG_RSAHEADER);  /* internal RSA header signature. */
define('RPMSIGTAG_SHA1',            RPMTAG_SHA1HEADER);  /* internal sha1 header digest. */
define('RPMSIGTAG_LONGSIZE',        RPMTAG_LONGSIGSIZE); /* internal Header+Payload size (64bit) in bytes. */
define('RPMSIGTAG_LONGARCHIVESIZE', RPMTAG_LONGARCHIVESIZE);  /* internal uncompressed payload size (64bit) in bytes. */
define('RPMSIGTAG_SHA256',          RPMTAG_SHA256HEADER);
define('RPMSIGTAG_FILESIGNATURES',  RPMTAG_FILESIGNATURESHEADER);
define('RPMSIGTAG_FILESIGNATURELENGTH',  RPMTAG_FILESIGNATURELENGTHHEADER);


?>

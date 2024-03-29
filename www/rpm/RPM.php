<?php
include('rpmtag.php');
include('rpmtagtbl.php');
require_once('PGP.php');

/*
 * RPM:
 * - lead (96 bytes)
 * - signature:
 *   - header (16 bytes)
 *   - index entries (each 16 bytes)
 *   - index data
 *   - padding to 8 bytes
 * - header:
 *   - header (16 bytes)
 *   - index entries (each 16 bytes)
 *   - index data
 *   - padding to 8 bytes
 * - payload data
 */


class RPM {
	private $filename = '';
	private $data = '';
	private $stream = 0;
	private $lead = 0;
	private $sig = 0;
	private $rpmh = 0;

	private static $arch_canon = array(
		0 => 'noarch',
		1 => 'x86_64',
		2 => 'alpha',
		3 => 'sparc',
		4 => 'mips',
		5 => 'ppc',
		6 => 'm68k',
		7 => 'sgi',
		8 => 'rs6000',
		9 => 'ia64',
		11 => 'mips64',
		12 => 'arm',
		13 => 'm68kmint',
		14 => 's390',
		15 => 's390x',
		16 => 'ppc64',
		17 => 'sh',
		18 => 'xtensa',
		19 => 'aarch64',
		20 => 'mipsr6',
		21 => 'mips64r6',
		22 => 'riscv',
	);

	private static $os_canon = array(
		0 => 'none',
		1 => 'linux',
		2 => 'irix',
		3 => 'solaris',
		4 => 'sunos',
		5 => 'aix',
		6 => 'hpux10',
		7 => 'osf1',
		8 => 'freebsd',
		9 => 'sco',
		10 => 'irix64',
		11 => 'nextstep',
		12 => 'bsdi',
		13 => 'machten',
		14 => 'cygwin32',
		15 => 'cygwin32',
		16 => 'mp_ras',
		17 => 'mint',
		18 => 'os390',
		19 => 'vm/esa',
		20 => 'os390',
		21 => 'darwin',
	);

	private static $sensesigns = array(
		RPMSENSE_ANY                      => '',
		RPMSENSE_EQUAL                    => '=',
		RPMSENSE_LESS                     => '<',
		RPMSENSE_GREATER                  => '>',
		RPMSENSE_GREATER | RPMSENSE_LESS  => '<>',
		RPMSENSE_LESS    | RPMSENSE_EQUAL => '<=',
		RPMSENSE_GREATER | RPMSENSE_EQUAL => '>=',
		RPMSENSE_GREATER | RPMSENSE_LESS | RPMSENSE_EQUAL => '<=>',
	);

	private static $type_names = array(
		RPM_TYPE_NULL => array('type' => RPM_TYPE_NULL, 'name' => 'NULL'),
		RPM_TYPE_CHAR => array('type' => RPM_TYPE_CHAR, 'name' => 'CHAR'),
		RPM_TYPE_INT8 => array('type' => RPM_TYPE_INT8, 'name' => 'INT8'),
		RPM_TYPE_INT16 => array('type' => RPM_TYPE_INT16, 'name' => 'INT16'),
		RPM_TYPE_INT32 => array('type' => RPM_TYPE_INT32, 'name' => 'INT32'),
		RPM_TYPE_INT64 => array('type' => RPM_TYPE_INT64, 'name' => 'INT64'),
		RPM_TYPE_STRING => array('type' => RPM_TYPE_STRING, 'name' => 'STRING'),
		RPM_TYPE_BIN => array('type' => RPM_TYPE_BIN , 'name' => 'BIN '),
		RPM_TYPE_STRING_ARRAY => array('type' => RPM_TYPE_STRING_ARRAY, 'name' => 'STRING_ARRAY'),
		RPM_TYPE_I18NSTRING => array('type' => RPM_TYPE_I18NSTRING, 'name' => 'I18NSTRING'),
		RPM_TYPE_ASN1 => array('type' => RPM_TYPE_ASN1, 'name' => 'ASN1'),
		RPM_TYPE_OPENPGP => array('type' => RPM_TYPE_OPENPGP, 'name' => 'OPENPGP'),
	);

	private function _close() : bool
	{
		if ($this->stream)
		{
			fclose($this->stream);
			$this->stream = 0;
		}
		/* data is retained until object is deleted */
		return true;
	}
	
	private function _open() : bool
	{
		if (!$this->stream)
		{
			$this->stream = fopen($this->filename, "rb");
			$this->data = '';
			$this->lead = 0;
		}
		if (!$this->stream)
		{
			return false;
		}
		return true;
	}
	
	private function _rpm_fread(int $size) : bool
	{
		$data = fread($this->stream, $size);
		if (strlen($data) != $size)
		{
			return false;
		}
		$this->data .= $data;
		return true;
	}
	
	private function _rpm_validity(bool $error_report) : bool
	{
		if (!$this->stream)
		{
			return false;
		}
		if (!$this->lead)
		{
			$this->data = '';
			if (!$this->_rpm_fread(96))
			{
				if ($error_report)
					trigger_error("File " . $this->filename . " is not an RPM file", E_USER_WARNING);
				return false;
			}
			if (PHP_VERSION_ID < 50500)
			{
				$this->lead = unpack("Nmagic/Cmajor/Cminor/ntype/narchnum/a66name/nosnum/nsignature_type" /* "/C16reserved" */, $this->data);
			} else
			{
				$this->lead = unpack("Nmagic/Cmajor/Cminor/ntype/narchnum/Z66name/nosnum/nsignature_type" /* "/C16reserved" */, $this->data);
			}
			if (isset(self::$arch_canon[$this->lead['archnum']]))
			{
				$this->lead['archname'] = self::$arch_canon[$this->lead['archnum']];
			} else
			{
				$this->lead['archname'] = 'unknown arch ' . $this->lead['archnum'];
			}
			if (isset(self::$os_canon[$this->lead['osnum']]))
			{
				$this->lead['osname'] = self::$os_canon[$this->lead['osnum']];
			} else
			{
				$this->lead['osname'] = 'unknown os ' . $this->lead['osnum'];
			}
		}
		if ($this->lead['magic'] != 0xedabeedb) /* RPMLEAD_MAGIC */
		{
			if ($error_report)
				trigger_error($this->filename . ": not an RPM file", E_USER_WARNING);
			return false;
		}
		if ($this->lead['signature_type'] != 5) /* RPMSIGTYPE_HEADERSIG */
		{
			if ($error_report)
				trigger_error($this->filename . ": illegal signature type", E_USER_WARNING);
			return false;
		}
		if ($this->lead['major'] < 3 || $this->lead['major'] > 4)
		{
			if ($error_report)
				trigger_error($this->filename . ": unsupported RPM package version", E_USER_WARNING);
			return false;
		}
		/* echo "<td><pre>\n"; print_r($this->lead); echo "</pre></td>\n";  */
		return true;
	}
	
	private function _rpm_fetch_header(int $offset)
	{
		if (!$this->_rpm_fread(16))
		{
			return 0;
		}
		$rh = unpack("C3magic/Cversion/Nreserved/Nnum_indices/Nstore_size", $this->data, $offset);
		if ($rh['magic1'] != 0x8e || $rh['magic2'] != 0xad || $rh['magic3'] != 0xe8 || /* HDR_MGK: rpm_header_magic */
			$rh['version'] != 1 ||
			$rh['reserved'] != 0)
		{
			return 0;
		}
		$rh['begin_byte'] = $offset;
		$datasize = $rh['num_indices'] * 16;
		if (!$this->_rpm_fread($datasize + $rh['store_size']))
		{
			return 0;
		}
		$rh['data_start'] = $offset + 16 + $datasize;
		return $rh;
	}
	
	private function _rpm_find_header() : int
	{
		$offset = 96;
		if (!($this->sig = $this->_rpm_fetch_header($offset)))
			return 0;
		/* printf("\nsignature header at 0x%x, num_indices=%u store_size=%x\n", $offset, $this->sig['num_indices'], $this->sig['store_size']); */
		$sigsize = 16 + $this->sig['num_indices'] * 16 + $this->sig['store_size'];
		$pad = (8 - ($sigsize % 8)) % 8;
		$offset += $sigsize + $pad;
		if ($pad != 0)
		{
			$this->_rpm_fread($pad);
		}
		return $offset;
	}
	
	private function _rpm_dump_header(array &$rh)
	{
		$count = $rh['num_indices'];
		printf("tag                                      type              offset     pos        count\n");
		$idxlist = &$rh['idxlist'];
		for ($i = 0; $i < $count; $i++)
		{
			printf("%-7u %-32s %-4u %-12s 0x%08x 0x%08x %u\n", $idxlist[$i]['tag'], self::tagname($idxlist[$i]['tag']), $idxlist[$i]['type'], self::typename($idxlist[$i]['type']), $idxlist[$i]['offset'], $idxlist[$i]['pos'], $idxlist[$i]['count']);
		}
	}

	function dump_header()
	{
		$this->_rpm_dump_header($this->rpmh);
	}

	private function _rpm_import_indices(array &$rh) : bool
	{
		$rh['idxlist'] = array();
		$idxlist = &$rh['idxlist'];
		$count = $rh['num_indices'];
		$offset = $rh['begin_byte'] + 16;
		$datastart = $rh['data_start'];
		for ($i = 0; $i < $count; $i++)
		{
			$idx = unpack("Ntag/Ntype/Noffset/Ncount", $this->data, $offset);
			$idx['pos'] = $idx['offset'] + $datastart;
			$offset += 16;
			array_push($idxlist, $idx);
		}
		return true;
	}
	
	/*
	 * Constructor
	 */
	public function __construct(string $filename)
	{
		$this->filename = $filename;
	}

	public function open() : bool
	{
		if (!$this->_open())
		{
			trigger_error("can't open " . $this->filename, E_USER_WARNING);
			return false;
		}
		if (!$this->_rpm_validity(true))
		{
			$this->_close();
			return false;
		}
		if (!($offset = $this->_rpm_find_header()))
		{
			trigger_error("RPM Header not found in " . $this->filename, E_USER_WARNING);
			$this->_close();
			return false;
		}
		if (!$this->_rpm_import_indices($this->sig))
		{
			trigger_error("Problem importing indices in " . $this->filename, E_USER_WARNING);
			$this->_close();
			return false;
		}
		/* $this->_rpm_dump_header($this->sig); */
		if (!($this->rpmh = $this->_rpm_fetch_header($offset)))
		{
			trigger_error("Cannot read header section in " . $this->filename, E_USER_WARNING);
			$this->_close();
			return false;
		}
		/* printf("payload header at 0x%x, num_indices=%u store_size=%x\n", $offset, $this->rpmh['num_indices'], $this->rpmh['store_size']); */
		if (!$this->_rpm_import_indices($this->rpmh))
		{
			trigger_error("Problem importing indices in " . $this->filename, E_USER_WARNING);
			$this->_close();
			return false;
		}
		/* $this->_rpm_dump_header($this->rpmh); */
		return true;
	}
	
	/*
	 * Destructor
	 */
	public function __destruct()
	{
		$this->_close();
		unset($this->filename);
		unset($this->data);
		unset($this->stream);
		unset($this->lead);
		unset($this->sig);
		unset($this->rpmh);
	}

	public function is_valid() : bool
	{
		if (!$this->_open())
		{
			return false;
		}
		if (!$this->_rpm_validity(false))
		{
			return false;
		}
		return true;
	}
	
	public function is_source() : bool
	{
		return $this->lead['type'] == 1; /* RPMLEAD_SOURCE */
	}
	
	public function name() : string
	{
		return $this->lead['name'];
	}
	
	public static function version() : string
	{
		return '0.4.0';
	}
	
	public static function tagname(int $tagnum) : string
	{
		global $rpmtagtbl;
		if (isset($rpmtagtbl[$tagnum]))
			return $rpmtagtbl[$tagnum]['name'];
		return 'unknown tag ' . $tagnum;
	}
	
	public static function typename(int $type) : string
	{
		if (isset(self::$type_names[$type]))
			return self::$type_names[$type]['name'];
		return 'unknown type ' . $type;
	}
	
	public static function requireflags(int $flags) : string
	{
		if (isset(self::$sensesigns[$flags & RPMSENSE_SENSEMASK]))
			return self::$sensesigns[$flags & RPMSENSE_SENSEMASK];
		return '';
	}
	
	public function get_tag_as_string(int $tagnum, bool $first_lang = false)
	{
		$s = $this->get_tag($tagnum);
		if (is_array($s))
		{
			if ($first_lang)
				$s = $s[0];
			else
				$s = implode("\n", $s);
		}
		return $s;
	}

	public function perm_string(int $mode) : string
	{
		switch (($mode >> 12) & 0x0f)
		{
			case 8: $perm = '-'; break;
			case 4: $perm = 'd'; break;
			case 10: $perm = 'l'; break;
			case 1: $perm = 'p'; break;
			case 12: $perm = 's'; break;
			case 2: $perm = 'c'; break;
			case 6: $perm = 'b'; break;
			/* bug from old versions of atari cpio: */
			case 14: $perm = 'l'; break;
			default: $perm = '?'; break;
		}
		$perm .= $mode & 0x100 ? 'r' : '-';
		$perm .= $mode & 0x080 ? 'w' : '-';
		$perm .= $mode & 0x800 ? ($mode & 0x040 ? 's' : 'S') : ($mode & 0x040 ? 'x' : '-');
		$perm .= $mode & 0x020 ? 'r' : '-';
		$perm .= $mode & 0x010 ? 'w' : '-';
		$perm .= $mode & 0x400 ? ($mode & 0x008 ? 's' : 'S') : ($mode & 0x008 ? 'x' : '-');
		$perm .= $mode & 0x004 ? 'r' : '-';
		$perm .= $mode & 0x002 ? 'w' : '-';
		$perm .= $mode & 0x200 ? ($mode & 0x001 ? 't' : 'T') : ($mode & 0x001 ? 'x' : '-');
		return $perm;
	}

	public function filesize_string($size)
	{
		if (is_null($size))
			return null;
		if ($size < 1024)
			return round($size) . "B";
		$size /= 1024;
		if ($size < 1024)
			return round($size,1) . "KB";
		$size /= 1024;
		if ($size < 1024)
			return round($size,1) . "MB";
		$size /= 1024;
		if ($size < 1024)
			return round($size,1) . "GB";
		$size /= 1024;
		return round($size,1) . "TB";
	}

	private function _get_tag(int $tagnum, bool $return_as_array, array &$rh)
	{
		$idxlist = &$rh['idxlist'];
		$count = $rh['num_indices'];
		for ($i = 0; $i < $count; $i++)
		{
			if ($idxlist[$i]['tag'] == $tagnum)
			{
				$datacount = $idxlist[$i]['count'];
				$offset = $idxlist[$i]['pos'];
				switch ($idxlist[$i]['type'])
				{
				case RPM_TYPE_NULL:
					return null;
				case RPM_TYPE_CHAR:
					return substr($this->data, $offset, $datacount);
				case RPM_TYPE_INT8:
				case RPM_TYPE_BIN:
				case RPM_TYPE_ASN1:
				case RPM_TYPE_OPENPGP:
					/*
					if ($datacount == 1 && !$return_as_array)
					{
						return ord($this->data[$offset]);
					}
					$a = array();
					for ($j = 0; $j < $datacount; $j++)
					{
						array_push($a, ord($this->data[$offset]));
						$offset++;
					}
					return $a;
					*/
					return substr($this->data, $offset, $datacount);
				case RPM_TYPE_INT16:
					if ($datacount == 1 && !$return_as_array)
					{
						$n = unpack("n", $this->data, $offset);
						return $n[1];
					}
					$a = array();
					for ($j = 0; $j < $datacount; $j++)
					{
						$n = unpack("n", $this->data, $offset);
						array_push($a, $n[1]);
						$offset += 2;
					}
					return $a;
				case RPM_TYPE_INT32:
					if ($datacount == 1 && !$return_as_array)
					{
						$n = unpack("N", $this->data, $offset);
						return $n[1];
					}
					$a = array();
					for ($j = 0; $j < $datacount; $j++)
					{
						$n = unpack("N", $this->data, $offset);
						array_push($a, $n[1]);
						$offset += 4;
					}
					return $a;
				case RPM_TYPE_INT64:
					if ($datacount == 1 && !$return_as_array)
					{
						$n = unpack("J", $this->data, $offset);
						return $n[1];
					}
					$a = array();
					for ($j = 0; $j < $datacount; $j++)
					{
						$n = unpack("J", $this->data, $offset);
						array_push($a, $n[1]);
						$offset += 8;
					}
					return $a;
				case RPM_TYPE_STRING:
				case RPM_TYPE_STRING_ARRAY:
				case RPM_TYPE_I18NSTRING:
					$a = array();
					for ($j = 0; $j < $datacount; $j++)
					{
						$n = unpack("Z*", $this->data, $offset);
						$s = $n[1];
						array_push($a, $s);
						$offset += strlen($s) + 1;
					}
					return $a;
				default:
					trigger_error($this->filename . ": invalid data type " . $idxlist[$i]['type'] . " in tag " . sprintf("0x%x", $idxlist[$i]['tag']), E_USER_WARNING);
					return null;
				}
			}
		}
		return null;
	}

	public function get_tag(int $tagnum, bool $return_as_array = false)
	{
		if (!$this->rpmh)
			return null;
		return $this->_get_tag($tagnum, $return_as_array, $this->rpmh);
	}

	public function get_signature()
	{
		if (!$this->sig)
			return null;
		$sig = $this->_get_tag(RPMTAG_DSAHEADER, false, $this->sig);
		if (is_null($sig))
			$sig = $this->_get_tag(RPMTAG_RSAHEADER, false, $this->sig);
		if (is_null($sig))
			$sig = $this->_get_tag(RPMTAG_SIGGPG, false, $this->sig);
		if (is_null($sig))
			$sig = $this->_get_tag(RPMTAG_SIGPGP, false, $this->sig);
		if (is_null($sig))
			return null;
		try {
			$pgp = new PGP($sig);
			$sigp = array();
			if ($pgp->prt_params(PGPTAG_SIGNATURE, $sigp))
				throw new Exception("not an OpenPGP signature");
			$key_algo = $pgp->dig_params_algo($sigp, PGPVAL_PUBKEYALGO);
			$hash_algo = $pgp->dig_params_algo($sigp, PGPVAL_HASHALGO);
			$dbuf = usertime($sigp['time'], 'ddd MMM DD YYYY HH:mm:ss ZZ');
			$keyid = $pgp->hexstr($sigp['signid']);
			$val = sprintf("V%d %s/%s, %s, Key ID %s", $sigp['version'], $pgp->val_string(PGPVAL_PUBKEYALGO, $key_algo), $pgp->val_string(PGPVAL_HASHALGO, $hash_algo), $dbuf, $keyid);
			return $val;
		} catch (Exception $e)
		{
			if (defined('STDERR'))
				fprintf(STDERR, "%s\n", $e->getMessage());
			return $e->getMessage();
		}
	}
}

function rpm_version() : string
{
	return RPM::version();
}

function rpm_open(string $filename)
{
	try {
		$rsrc = new RPM($filename);
		if (!$rsrc->open())
			return null;
	} catch (Exception $e)
	{
		return null;
	}
	return $rsrc;
}

function rpm_close($rsrc) : bool
{
	unset($rsrc);
	return true;
}

function rpm_get_tag($rsrc, int $tagnum)
{
	return $rsrc->get_tag($tagnum);
}

function rpm_is_valid(string $filename) : bool
{
	try {	
		$rsrc = new RPM($filename);
		$rsrc->open();
		$status = $rsrc->is_valid();
		unset($rsrc);
		return $status;
	} catch (Exception $e)
	{
		return false;
	}
}

?>

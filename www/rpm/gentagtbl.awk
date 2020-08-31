/[\t ](RPMTAG_[A-Z0-9]*)[ \t]+([0-9]*)/ && !/internal/ && !/unimplemented/ && !/alias/ {
	tt = "NULL"
	ta = "ANY"
	ext = "0"
	if ($5 == "c") {
		tt = "CHAR"
		ta = "SCALAR"
	}
	if ($5 == "c[]") {
		tt = "CHAR"
		ta = "ARRAY"
	} 
	if ($5 == "h") {
		tt = "INT16"
		ta = "SCALAR"
	}
	if ($5 == "h[]") {
		tt = "INT16"
		ta = "ARRAY"
	}
	if ($5 == "i") {
		tt = "INT32"
		ta = "SCALAR"
	}
	if ($5 == "i[]") {
		tt = "INT32"
		ta = "ARRAY"
	}
	if ($5 == "l") {
		tt = "INT64"
		ta = "SCALAR"
	}
	if ($5 == "l[]") {
		tt = "INT64"
		ta = "ARRAY"
	}
	if ($5 == "s") {
		tt = "STRING"
		ta = "SCALAR"
	}
	if ($5 == "s[]") {
		tt = "STRING_ARRAY"
		ta = "ARRAY"
	}
	if ($5 == "s{}") {
		tt = "I18NSTRING"
		ta = "SCALAR"
	} 
	if ($5 == "x") {
		tt = "BIN"
		ta = "SCALAR"
	}
	if ($6 == "extension") {
		ext = "1"
	}
	if ($2 == "=") {
		tnarg = $1
	} else {
		tnarg = $2
	}
	tn = substr(tnarg, index(tnarg, "_") + 1)
	sn = (substr(tn, 1, 1) tolower(substr(tn, 2)))
	if ($2 == "=") {
		value = tnarg;
	} else {
		value = $3;
	}
	printf("\t%s => array('tag' => %s, 'name' => '%s', 'specname' => '%s', 'type' => RPM_TYPE_%s, 'returntype' => RPM_%s_RETURN_TYPE, 'extension' => %d),\n", tnarg, tnarg, tnarg, sn, tt, ta, ext)
}

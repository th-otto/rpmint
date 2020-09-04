<?php

/*
 https://tools.ietf.org/html/rfc2440
 https://tools.ietf.org/html/rfc4880
 https://tools.ietf.org/html/rfc5581
 https://datatracker.ietf.org/doc/draft-ietf-openpgp-rfc4880bis/
*/

/*
 * Packet Tags
 *
 * The packet tag denotes what type of packet the body holds. Note that
 * old format headers can only have tags less than 16, whereas new
 * format headers can have tags as great as 63.
 */
define('PGPTAG_RESERVED',              0);  /* Reserved/Invalid */
define('PGPTAG_PUBLIC_SESSION_KEY',    1);  /* Public-Key Encrypted Session Key */
define('PGPTAG_SIGNATURE',             2);  /* Signature */
define('PGPTAG_SYMMETRIC_SESSION_KEY', 3);  /* Symmetric-Key Encrypted Session Key */
define('PGPTAG_ONEPASS_SIGNATURE',     4);  /* One-Pass Signature */
define('PGPTAG_SECRET_KEY',            5);  /* Secret Key */
define('PGPTAG_PUBLIC_KEY',            6);  /* Public Key */
define('PGPTAG_SECRET_SUBKEY',         7);  /* Secret Subkey */
define('PGPTAG_COMPRESSED_DATA',       8);  /* Compressed Data */
define('PGPTAG_SYMMETRIC_DATA',        9);  /* Symmetrically Encrypted Data */
define('PGPTAG_MARKER',                10); /* Marker */
define('PGPTAG_LITERAL_DATA',          11); /* Literal Data */
define('PGPTAG_TRUST',                 12); /* Trust */
define('PGPTAG_USER_ID',               13); /* User ID */
define('PGPTAG_PUBLIC_SUBKEY',         14); /* Public Subkey */
define('PGPTAG_COMMENT_OLD',           16); /* Comment (from OpenPGP draft) */
define('PGPTAG_PHOTOID',               17); /* PGP's photo ID */
define('PGPTAG_ENCRYPTED_MDC',         18); /* Integrity protected encrypted data */
define('PGPTAG_MDC',                   19); /* Manipulaion detection code packet */
define('PGPTAG_ENCRYPTED_AEAD',        20); /* /* AEAD encrypted data packet */
define('PGPTAG_PRIVATE_60',            60); /* Private or Experimental Values */
define('PGPTAG_COMMENT',               61); /* Comment */
define('PGPTAG_PRIVATE_62',            62); /* Private or Experimental Values */
define('PGPTAG_CONTROL',               63); /* Control (GPG) */

/*
 * Signature Types
 *
 * There are a number of possible meanings for a signature, which are
 * specified in a signature type octet in any given signature.
 */
define('PGPSIGTYPE_BINARY',                0x00); /* Binary document */
define('PGPSIGTYPE_TEXT',                  0x01); /* Canonical text document */
define('PGPSIGTYPE_STANDALONE',            0x02); /* Standalone */
define('PGPSIGTYPE_GENERIC_CERT',          0x10); /* Generic certification of a User ID & Public Key */
define('PGPSIGTYPE_PERSONA_CERT',          0x11); /* Persona certification of a User ID & Public Key */
define('PGPSIGTYPE_CASUAL_CERT',           0x12); /* Casual certification of a User ID & Public Key */
define('PGPSIGTYPE_POSITIVE_CERT',         0x13); /* Positive certification of a User ID & Public Key */
define('PGPSIGTYPE_SUBKEY_BINDING',        0x18); /* Subkey Binding */
define('PGPSIGTYPE_SIGNED_KEY',            0x1F); /* Signature directly on a key */
define('PGPSIGTYPE_KEY_REVOKE',            0x20); /* Key revocation */
define('PGPSIGTYPE_SUBKEY_REVOKE',         0x28); /* Subkey revocation */
define('PGPSIGTYPE_CERT_REVOKE',           0x30); /* Certification revocation */
define('PGPSIGTYPE_TIMESTAMP',             0x40); /* Timestamp */
define('PGPSIGTYPE_3RDPARTY_CONFIRMATION', 0x50); /* Third-Party Confirmation signature */

/*
 * Public Key Algorithms
 *
 * Implementations MUST implement DSA for signatures, and Elgamal for
 * encryption. Implementations SHOULD implement RSA keys.
 * Implementations MAY implement any other algorithm.
 */
define('PGPPUBKEYALGO_RSA',             1);  /* RSA */
define('PGPPUBKEYALGO_RSA_ENCRYPT',     2);  /* RSA(Encrypt-Only) */
define('PGPPUBKEYALGO_RSA_SIGN',        3);  /* RSA(Sign-Only) */
define('PGPPUBKEYALGO_ELGAMAL_ENCRYPT', 16); /* Elgamal(Encrypt-Only) */
define('PGPPUBKEYALGO_DSA',             17); /* DSA */
define('PGPPUBKEYALGO_EC',              18); /* Elliptic Curve */
define('PGPPUBKEYALGO_ECDSA',           19); /* ECDSA */
define('PGPPUBKEYALGO_ELGAMAL',         20); /* Elgamal */
define('PGPPUBKEYALGO_DH',              21); /* Diffie-Hellman (X9.42) */
define('PGPPUBKEYALGO_EDDSA',           22); /* EdDSA (not yet assigned) */


/*
 * Symmetric Key Algorithms
 *
 * Implementations MUST implement Triple-DES. Implementations SHOULD
 * implement IDEA and CAST5. Implementations MAY implement any other
 * algorithm.
 */
define('PGPSYMKEYALGO_PLAINTEXT',    0);   /* Plaintext */
define('PGPSYMKEYALGO_IDEA',         1);   /* IDEA */
define('PGPSYMKEYALGO_TRIPLE_DES',   2);   /* 3DES */
define('PGPSYMKEYALGO_CAST5',        3);   /* CAST5 */
define('PGPSYMKEYALGO_BLOWFISH',     4);   /* BLOWFISH */
define('PGPSYMKEYALGO_SAFER',        5);   /* SAFER */
define('PGPSYMKEYALGO_DES_SK',       6);   /* DES/SK */
define('PGPSYMKEYALGO_AES_128',      7);   /* AES(128-bit key) */
define('PGPSYMKEYALGO_AES_192',      8);   /* AES(192-bit key) */
define('PGPSYMKEYALGO_AES_256',      9);   /* AES(256-bit key) */
define('PGPSYMKEYALGO_TWOFISH',      10);  /* TWOFISH(256-bit key) */
define('PGPSYMKEYALGO_CAMELLIA128',  11);  /* Camellia(128-bit key) */
define('PGPSYMKEYALGO_CAMELLIA192',  12);  /* Camellia(192-bit key) */
define('PGPSYMKEYALGO_CAMELLIA256',  13);  /* Camellia(256-bit key) */
define('PGPSYMKEYALGO_NOENCRYPT',    110); /* no encryption */

/*
 * Compression Algorithms
 *
 * Implementations MUST implement uncompressed data. Implementations
 * SHOULD implement ZIP. Implementations MAY implement ZLIB.
 */
define('PGPCOMPRESSALGO_NONE',      0); /* Uncompressed */
define('PGPCOMPRESSALGO_ZIP',       1); /* ZIP */
define('PGPCOMPRESSALGO_ZLIB',      2); /* ZLIB */
define('PGPCOMPRESSALGO_BZIP2',     3);   /* BZIP2 */
define('PGPCOMPRESSALGO_PRIVATE10', 110); /* Private */

/*
 * Hash Algorithms
 *
 * Implementations MUST implement SHA-1. Implementations SHOULD
 * implement MD5.
 */
define('PGPHASHALGO_MD5',         1);  /* MD5 */
define('PGPHASHALGO_SHA1',        2);  /* SHA1 */
define('PGPHASHALGO_RIPEMD160',   3);  /* RIPEMD160 */
define('PGPHASHALGO_SHA2',        4);  /* double-width SHA (experimental) */
define('PGPHASHALGO_MD2',         5);  /* MD2 */
define('PGPHASHALGO_TIGER192',    6);  /* TIGER192 */
define('PGPHASHALGO_HAVAL_5_160', 7);  /* HAVAL-5-160 */
define('PGPHASHALGO_SHA256',      8);  /* SHA256 */
define('PGPHASHALGO_SHA384',      9);  /* SHA384 */
define('PGPHASHALGO_SHA512',      10); /* SHA512 */
define('PGPHASHALGO_SHA224',      11); /* SHA224 */
define('PGPHASHALGO_PRIVATE10',   110); /* Private */

/*
 * 5.2.3.1. Signature Subpacket Specification
 *
 * The subpacket fields consist of zero or more signature subpackets.
 * Each set of subpackets is preceded by a two-octet scalar count of the
 * length of the set of subpackets.
 *
 * Each subpacket consists of a subpacket header and a body.  The header
 * consists of:
 *   - the subpacket length (1,  2, or 5 octets)
 *   - the subpacket type (1 octet)
 * and is followed by the subpacket specific data.
 *
 * The length includes the type octet but not this length. Its format is
 * similar to the "new" format packet header lengths, but cannot have
 * partial body lengths. That is:
 *
 * An implementation SHOULD ignore any subpacket of a type that it does
 * not recognize.
 *
 * Bit 7 of the subpacket type is the "critical" bit.  If set, it
 * denotes that the subpacket is one that is critical for the evaluator
 * of the signature to recognize.  If a subpacket is encountered that is
 * marked critical but is unknown to the evaluating software, the
 * evaluator SHOULD consider the signature to be in error.
 *
 * The value of the subpacket type octet may be:
 */
define('PGPSUBTYPE_NONE',                    0);   /* none */
define('PGPSUBTYPE_SIG_CREATE_TIME',         2);   /* signature creation time */
define('PGPSUBTYPE_SIG_EXPIRE_TIME',         3);   /* signature expiration time */
define('PGPSUBTYPE_EXPORTABLE_CERT',         4);   /* exportable certification */
define('PGPSUBTYPE_TRUST_SIG',               5);   /* trust signature */
define('PGPSUBTYPE_REGEX',                   6);   /* regular expression */
define('PGPSUBTYPE_REVOCABLE',               7);   /* revocable */
define('PGPSUBTYPE_KEY_EXPIRE_TIME',         9);   /* key expiration time */
define('PGPSUBTYPE_ARR',                     10);  /* additional recipient request */
define('PGPSUBTYPE_PREFER_SYMKEY',           11);  /* preferred symmetric algorithms */
define('PGPSUBTYPE_REVOKE_KEY',              12);  /* revocation key */
define('PGPSUBTYPE_ISSUER_KEYID',            16);  /* issuer key ID */
define('PGPSUBTYPE_NOTATION',                20);  /* notation data */
define('PGPSUBTYPE_PREFER_HASH',             21);  /* preferred hash algorithms */
define('PGPSUBTYPE_PREFER_COMPRESS',         22);  /* preferred compression algorithms */
define('PGPSUBTYPE_KEYSERVER_PREFERS',       23);  /* key server preferences */
define('PGPSUBTYPE_PREFER_KEYSERVER',        24);  /* preferred key server */
define('PGPSUBTYPE_PRIMARY_USERID',          25);  /* primary user id */
define('PGPSUBTYPE_POLICY_URL',              26);  /* policy URL */
define('PGPSUBTYPE_KEY_FLAGS',               27);  /* key flags */
define('PGPSUBTYPE_SIGNER_USERID',           28);  /* signer's user id */
define('PGPSUBTYPE_REVOKE_REASON',           29);  /* reason for revocation */
define('PGPSUBTYPE_FEATURES',                30);  /* feature flags (gpg) */
define('PGPSUBTYPE_EMBEDDED_SIG',            32);  /* embedded signature (gpg) */
define('PGPSUBTYPE_ISSUER_FINGERPRINT',      33);  /* Issuer fingerprint */
define('PGPSUBTYPE_PREF_AEAD',               34);  /* Preferred AEAD algorithms */
define('PGPSUBTYPE_RECIPIENT_FINGERPRINT',   35);  /* Intended Recipient Fingerprint */
define('PGPSUBTYPE_ATTESTED_CERTIFICATIONS', 37);  /* Attested Certifications */
define('PGPSUBTYPE_KEY_BLOCK',               38);  /* Entire key used */

define('PGPSUBTYPE_INTERNAL_100',      100); /* internal or user-defined */
define('PGPSUBTYPE_INTERNAL_101',      101); /* internal or user-defined */
define('PGPSUBTYPE_INTERNAL_102',      102); /* internal or user-defined */
define('PGPSUBTYPE_INTERNAL_103',      103); /* internal or user-defined */
define('PGPSUBTYPE_INTERNAL_104',      104); /* internal or user-defined */
define('PGPSUBTYPE_INTERNAL_105',      105); /* internal or user-defined */
define('PGPSUBTYPE_INTERNAL_106',      106); /* internal or user-defined */
define('PGPSUBTYPE_INTERNAL_107',      107); /* internal or user-defined */
define('PGPSUBTYPE_INTERNAL_108',      108); /* internal or user-defined */
define('PGPSUBTYPE_INTERNAL_109',      109); /* internal or user-defined */
define('PGPSUBTYPE_INTERNAL_110',      110); /* internal or user-defined */
define('PGPSUBTYPE_CRITICAL',          128); /* critical subpacket marker */

define('PGPARMOR_ERR_CRC_CHECK',            -7);
define('PGPARMOR_ERR_BODY_DECODE',          -6);
define('PGPARMOR_ERR_CRC_DECODE',           -5);
define('PGPARMOR_ERR_NO_END_PGP',           -4);
define('PGPARMOR_ERR_UNKNOWN_PREAMBLE_TAG', -3);
define('PGPARMOR_ERR_UNKNOWN_ARMOR_TYPE',   -2);
define('PGPARMOR_ERR_NO_BEGIN_PGP',         -1);
define('PGPARMOR_ERROR',                    PGPARMOR_ERR_NO_BEGIN_PGP);
define('PGPARMOR_NONE',                     0);
define('PGPARMOR_MESSAGE',                  1); /* MESSAGE */
define('PGPARMOR_PUBKEY',                   2); /* PUBLIC KEY BLOCK */
define('PGPARMOR_SIGNATURE',                3); /* SIGNATURE */
define('PGPARMOR_SIGNED_MESSAGE',           4); /* SIGNED MESSAGE */
define('PGPARMOR_FILE',                     5); /* ARMORED FILE */
define('PGPARMOR_PRIVKEY',                  6); /* PRIVATE KEY BLOCK */
define('PGPARMOR_SECKEY',                   7); /* SECRET KEY BLOCK */

define('PGPARMORKEY_VERSION',   1); /* Version: */
define('PGPARMORKEY_COMMENT',   2); /* Comment: */
define('PGPARMORKEY_MESSAGEID', 3); /* MessageID: */
define('PGPARMORKEY_HASH',      4); /* Hash: */
define('PGPARMORKEY_CHARSET',   5); /* Charset: */

define('PGPVAL_TAG',          1);
define('PGPVAL_ARMORBLOCK',   2);
define('PGPVAL_ARMORKEY',     3);
define('PGPVAL_SIGTYPE',      4);
define('PGPVAL_SUBTYPE',      5);
define('PGPVAL_PUBKEYALGO',   6);
define('PGPVAL_SYMKEYALGO',   7);
define('PGPVAL_COMPRESSALGO', 8);
define('PGPVAL_HASHALGO',     9);
define('PGPVAL_SERVERPREFS',  10);

/*
 * Bit(s) to control digest operation.
 */
define('PGPDIGEST_NONE', 0);

define('PGPDIG_SAVED_TIME', 0x01);
define('PGPDIG_SAVED_ID',   0x02);


class PGP_digest_null {
	public $mpis = -1;
	public function setmpi(int $num, string $p) : int
	{
		return 0;
	}
	public function verify($pgpsig, string $hash, int $hash_algo) : int
	{
		return 0;
	}
}


class PGP_digest_rsa {
	public $mpis = 1;
	public function setmpi(int $num, string $p) : int
	{
		return 0;
	}
	public function verify($pgpsig, string $hash, int $hash_algo) : int
	{
		return 0;
	}
	public function reset() : int
	{
		return 0;
	}
}


class PGP_digest_dsa {
	public $mpis = 2;
	public function setmpi(int $num, string $p) : int
	{
		return 0;
	}
	public function verify($pgpsig, string $hash, int $hash_algo) : int
	{
		return 0;
	}
	public function reset() : int
	{
		return 0;
	}
}


class PGP_digest_md5 {
	public $digestlen = 16;
	public $datalen = 64;
	public $flags = 0;
	public function reset() : int
	{
		return 0;
	}
	public function update(string $in, int $len) : int
	{
		return 0;
	}
	public function final(bool $asascii) : string
	{
		return '';
	}
}


class PGP_digest_sha1 {
	public $digestlen = 20;
	public $datalen = 64;
	public $flags = 0;
	public function reset() : int
	{
		return 0;
	}
	public function update(string $in, int $len) : int
	{
		return 0;
	}
	public function final(bool $asascii) : string
	{
		return '';
	}
}


class PGP_digest_sha256 {
	public $digestlen = 32;
	public $datalen = 64;
	public $flags = 0;
	public function reset() : int
	{
		return 0;
	}
	public function update(string $in, int $len) : int
	{
		return 0;
	}
	public function final(bool $asascii) : string
	{
		return '';
	}
}


class PGP_digest_sha384 {
	public $digestlen = 48;
	public $datalen = 128;
	public $flags = 0;
	public function reset() : int
	{
		return 0;
	}
	public function update(string $in, int $len) : int
	{
		return 0;
	}
	public function final(bool $asascii) : string
	{
		return '';
	}
}


class PGP_digest_sha512 {
	public $digestlen = 64;
	public $datalen = 128;
	public $flags = 0;
	public function reset() : int
	{
		return 0;
	}
	public function update(string $in, int $len) : int
	{
		return 0;
	}
	public function final(bool $asascii) : string
	{
		return '';
	}
}


class PGP_pubkey_null {
	public $mpis = -1;
	public function setmpi(int $num, string $p) : int
	{
		return 0;
	}
	public function verify($pgpsig, string $hash, int $hash_algo) : int
	{
		return 0;
	}
}


class PGP_pubkey_rsa {
	public $mpis = 2;
	public function setmpi(int $num, string $p) : int
	{
		return 0;
	}
	public function verify($pgpsig, string $hash, int $hash_algo) : int
	{
		return 0;
	}
}


class PGP_pubkey_dsa {
	public $mpis = 4;
	public function setmpi(int $num, string $p) : int
	{
		return 0;
	}
	public function verify($pgpsig, string $hash, int $hash_algo) : int
	{
		return 0;
	}
}


class PGP {
	private $data;
	private $datalen;
	private $_print = false;

	private static $valtbl = array(
		PGPVAL_TAG => array(
			PGPTAG_PUBLIC_SESSION_KEY => "Public-Key Encrypted Session Key",
			PGPTAG_SIGNATURE => "Signature",
			PGPTAG_SYMMETRIC_SESSION_KEY => "Symmetric-Key Encrypted Session Key",
			PGPTAG_ONEPASS_SIGNATURE => "One-Pass Signature",
			PGPTAG_SECRET_KEY => "Secret Key",
			PGPTAG_PUBLIC_KEY => "Public Key",
			PGPTAG_SECRET_SUBKEY => "Secret Subkey",
			PGPTAG_COMPRESSED_DATA => "Compressed Data",
			PGPTAG_SYMMETRIC_DATA => "Symmetrically Encrypted Data",
			PGPTAG_MARKER => "Marker",
			PGPTAG_LITERAL_DATA => "Literal Data",
			PGPTAG_TRUST => "Trust",
			PGPTAG_USER_ID => "User ID",
			PGPTAG_PUBLIC_SUBKEY => "Public Subkey",
			PGPTAG_COMMENT_OLD => "Comment (from OpenPGP draft)",
			PGPTAG_PHOTOID => "PGP's photo ID",
			PGPTAG_ENCRYPTED_MDC => "Integrity protected encrypted data",
			PGPTAG_MDC => "Manipulaion detection code packet",
			PGPTAG_ENCRYPTED_AEAD => "AEAD encrypted data packet",
			PGPTAG_PRIVATE_60 => "Private #60",
			PGPTAG_COMMENT => "Comment",
			PGPTAG_PRIVATE_62 => "Private #62",
			PGPTAG_CONTROL => "Control (GPG)",
			-1 => "Unknown packet tag",
		),

		PGPVAL_ARMORBLOCK => array(
			PGPARMOR_MESSAGE => "MESSAGE",
			PGPARMOR_PUBKEY => "PUBLIC KEY BLOCK",
			PGPARMOR_SIGNATURE => "SIGNATURE",
			PGPARMOR_SIGNED_MESSAGE => "SIGNED MESSAGE",
			PGPARMOR_FILE => "ARMORED FILE",
			PGPARMOR_PRIVKEY => "PRIVATE KEY BLOCK",
			PGPARMOR_SECKEY => "SECRET KEY BLOCK",
			-1 => "Unknown armor block"
		),

		PGPVAL_ARMORKEY => array(
			PGPARMORKEY_VERSION => "Version: ",
			PGPARMORKEY_COMMENT => "Comment: ",
			PGPARMORKEY_MESSAGEID => "MessageID: ",
			PGPARMORKEY_HASH => "Hash: ",
			PGPARMORKEY_CHARSET => "Charset: ",
			-1 => "Unknown armor key"
		),

		PGPVAL_SIGTYPE => array(
			PGPSIGTYPE_BINARY => "Binary document signature",
			PGPSIGTYPE_TEXT => "Text document signature",
			PGPSIGTYPE_STANDALONE => "Standalone signature",
			PGPSIGTYPE_GENERIC_CERT => "Generic certification of a User ID and Public Key",
			PGPSIGTYPE_PERSONA_CERT => "Persona certification of a User ID and Public Key",
			PGPSIGTYPE_CASUAL_CERT => "Casual certification of a User ID and Public Key",
			PGPSIGTYPE_POSITIVE_CERT => "Positive certification of a User ID and Public Key",
			PGPSIGTYPE_SUBKEY_BINDING => "Subkey Binding Signature",
			PGPSIGTYPE_SIGNED_KEY => "Signature directly on a key",
			PGPSIGTYPE_KEY_REVOKE => "Key revocation signature",
			PGPSIGTYPE_SUBKEY_REVOKE => "Subkey revocation signature",
			PGPSIGTYPE_CERT_REVOKE => "Certification revocation signature",
			PGPSIGTYPE_TIMESTAMP => "Timestamp signature",
			PGPSIGTYPE_3RDPARTY_CONFIRMATION => "Third-Party Confirmation signature",
			-1 => "Unknown signature type",
		),

		PGPVAL_SUBTYPE => array(
			PGPSUBTYPE_SIG_CREATE_TIME => "signature creation time",
			PGPSUBTYPE_SIG_EXPIRE_TIME => "signature expiration time",
			PGPSUBTYPE_EXPORTABLE_CERT => "exportable certification",
			PGPSUBTYPE_TRUST_SIG => "trust signature",
			PGPSUBTYPE_REGEX => "regular expression",
			PGPSUBTYPE_REVOCABLE => "revocable",
			PGPSUBTYPE_KEY_EXPIRE_TIME => "key expiration time",
			PGPSUBTYPE_ARR => "additional recipient request",
			PGPSUBTYPE_PREFER_SYMKEY => "preferred symmetric algorithms",
			PGPSUBTYPE_REVOKE_KEY => "revocation key",
			PGPSUBTYPE_ISSUER_KEYID => "issuer key ID",
			PGPSUBTYPE_NOTATION => "notation data",
			PGPSUBTYPE_PREFER_HASH => "preferred hash algorithms",
			PGPSUBTYPE_PREFER_COMPRESS => "preferred compression algorithms",
			PGPSUBTYPE_KEYSERVER_PREFERS => "key server preferences",
			PGPSUBTYPE_PREFER_KEYSERVER => "preferred key server",
			PGPSUBTYPE_PRIMARY_USERID => "primary user id",
			PGPSUBTYPE_POLICY_URL => "policy URL",
			PGPSUBTYPE_KEY_FLAGS => "key flags",
			PGPSUBTYPE_SIGNER_USERID => "signer's user id",
			PGPSUBTYPE_REVOKE_REASON => "reason for revocation",
			PGPSUBTYPE_FEATURES => "features",
			PGPSUBTYPE_EMBEDDED_SIG => "embedded signature",
			PGPSUBTYPE_ISSUER_FINGERPRINT => "issuer fingerprint",
			PGPSUBTYPE_PREF_AEAD => "preferred AEAD algorithms",
			PGPSUBTYPE_RECIPIENT_FINGERPRINT => "Intended Recipient Fingerprint",
			PGPSUBTYPE_ATTESTED_CERTIFICATIONS => "Attested Certifications",
			PGPSUBTYPE_KEY_BLOCK, "entire key used",
			
			PGPSUBTYPE_INTERNAL_100 => "internal subpkt type 100",
			PGPSUBTYPE_INTERNAL_101 => "internal subpkt type 101",
			PGPSUBTYPE_INTERNAL_102 => "internal subpkt type 102",
			PGPSUBTYPE_INTERNAL_103 => "internal subpkt type 103",
			PGPSUBTYPE_INTERNAL_104 => "internal subpkt type 104",
			PGPSUBTYPE_INTERNAL_105 => "internal subpkt type 105",
			PGPSUBTYPE_INTERNAL_106 => "internal subpkt type 106",
			PGPSUBTYPE_INTERNAL_107 => "internal subpkt type 107",
			PGPSUBTYPE_INTERNAL_108 => "internal subpkt type 108",
			PGPSUBTYPE_INTERNAL_109 => "internal subpkt type 109",
			PGPSUBTYPE_INTERNAL_110 => "internal subpkt type 110",
			-1 => "Unknown signature subkey type",
		),

		PGPVAL_PUBKEYALGO => array(
			PGPPUBKEYALGO_RSA => "RSA",
			PGPPUBKEYALGO_RSA_ENCRYPT => "RSA(Encrypt-Only)",
			PGPPUBKEYALGO_RSA_SIGN => "RSA(Sign-Only)",
			PGPPUBKEYALGO_ELGAMAL_ENCRYPT => "Elgamal(Encrypt-Only)",
			PGPPUBKEYALGO_DSA => "DSA",
			PGPPUBKEYALGO_EC => "Elliptic Curve",
			PGPPUBKEYALGO_ECDSA => "ECDSA",
			PGPPUBKEYALGO_ELGAMAL => "Elgamal",
			PGPPUBKEYALGO_DH => "Diffie-Hellman (X9.42)",
			PGPPUBKEYALGO_EDDSA => "EdDSA",
			-1 => "Unknown public key algorithm",
		),

		PGPVAL_SYMKEYALGO => array(
			PGPSYMKEYALGO_PLAINTEXT => "Plaintext",
			PGPSYMKEYALGO_IDEA => "IDEA",
			PGPSYMKEYALGO_TRIPLE_DES => "3DES",
			PGPSYMKEYALGO_CAST5 => "CAST5",
			PGPSYMKEYALGO_BLOWFISH => "BLOWFISH",
			PGPSYMKEYALGO_SAFER => "SAFER",
			PGPSYMKEYALGO_DES_SK => "DES/SK",
			PGPSYMKEYALGO_AES_128 => "AES(128-bit key)",
			PGPSYMKEYALGO_AES_192 => "AES(192-bit key)",
			PGPSYMKEYALGO_AES_256 => "AES(256-bit key)",
			PGPSYMKEYALGO_TWOFISH => "TWOFISH(256-bit key)",
			PGPSYMKEYALGO_CAMELLIA128 => "Camellia(128-bit key)",
			PGPSYMKEYALGO_CAMELLIA192 => "Camellia(192-bit key)",
			PGPSYMKEYALGO_CAMELLIA256 => "Camellia(256-bit key)",
			PGPSYMKEYALGO_NOENCRYPT => "no encryption",
			-1 => "Unknown symmetric key algorithm",
		),

		PGPVAL_COMPRESSALGO => array(
			PGPCOMPRESSALGO_NONE => "Uncompressed",
			PGPCOMPRESSALGO_ZIP => "ZIP",
			PGPCOMPRESSALGO_ZLIB => "ZLIB",
			PGPCOMPRESSALGO_BZIP2 => "BZIP2",
			PGPCOMPRESSALGO_PRIVATE10 => "Private10",
			-1 => "Unknown compression algorithm",
		),

		PGPVAL_HASHALGO => array(
			PGPHASHALGO_MD5 => "MD5",
			PGPHASHALGO_SHA1 => "SHA1",
			PGPHASHALGO_RIPEMD160 => "RIPEMD160",
			PGPHASHALGO_MD2 => "MD2",
			PGPHASHALGO_TIGER192 => "TIGER192",
			PGPHASHALGO_HAVAL_5_160 => "HAVAL-5-160",
			PGPHASHALGO_SHA256 => "SHA256",
			PGPHASHALGO_SHA384 => "SHA384",
			PGPHASHALGO_SHA512 => "SHA512",
			PGPHASHALGO_SHA224 => "SHA224",
			PGPHASHALGO_PRIVATE10 => "Private10",
			-1 => "Unknown hash algorithm",
		),

		PGPVAL_SERVERPREFS => array(
			0x80 => "No-modify",
			-1 => "Unknown key server preference",
		),
	);
	
	/*
	 * Constructor
	 */
	public function __construct(string $data)
	{
		$this->data = $data;
		$this->datalen = strlen($data);
	}

	public function dig_params_algo(array &$digp, int $algotype) : int
	{
		$algo = 0; /* assume failure */
		switch ($algotype)
		{
		case PGPVAL_PUBKEYALGO:
			if (isset($digp['pubkey_algo']))
				$algo = $digp['pubkey_algo'];
			break;
		case PGPVAL_HASHALGO:
			if (isset($digp['hash_algo']))
				$algo = $digp['hash_algo'];
			break;
		}
		return $algo;
	}

	public function val_string(int $type, int $val) : string
	{
		if (isset(self::$valtbl[$type][$val]))
			return self::$valtbl[$type][$val];
		return self::$valtbl[$type][-1];
	}

	private function prt_nl()
	{
		if (!$this->_print)
			return;
		if (!defined('STDERR'))
			return;
		fprintf(STDERR, "\n");
	}
	
	private function prt_hex(string $pre, string $p)
	{
		if (!$this->_print)
			return;
		if (!defined('STDERR'))
			return;
		if ($pre != '')
			fprintf(STDERR, "%s", $pre);
		$hex = self::hexstr($p);
		fprintf(STDERR, " %s", $hex);
	}

	private function prt_val(string $pre, int $type, int $val)
	{
		if (!$this->_print)
			return;
		if (!defined('STDERR'))
			return;
		if ($pre != '')
			fprintf(STDERR, "%s", $pre);
		fprintf(STDERR, "%s(%u)", $this->val_string($type, $val), $val);
	}

	/*
	 * Return (native-endian) integer from big-endian representation.
	 * @param s 	pointer to big-endian integer
	 * @return		native-endian integer
	 */
	private function grab(string $s) : int
	{
		$i = 0;
		$l = strlen($s);
		for ($j = 0; $j < $l; $j++)
			$i = ($i << 8) | (ord($s[$j]) & 255);
		return $i;
	}

	private function prt_time(string $pre, string $p)
	{
		if (!$this->_print)
			return;
		if (!defined('STDERR'))
			return;
		if ($pre != '')
			fprintf(STDERR, "%s", $pre);
		if (strlen($p) == 4)
		{
			$t = $this->grab($p);
			/*
			$localt = localtime($t, true);
			$localt = mktime($localt['tm_hour'], $localt['tm_min'], $localt['tm_sec'], $localt['tm_mon'] + 1, $localt['tm_mday'], $localt['tm_year'] + 1900);
			fprintf(STDERR, " %s (0x%08x)", strftime("%a %b %e %H:%M:%S %Y %z", localtime($localt)), $t);
			*/
			$dt = new DateTime("@$t");
			$zone = new DateTimeZone("Europe/Berlin");
			$dt->setTimezone($zone);
			$loc = $zone->getLocation();
			$localt = $t + $dt->getOffset();
			fprintf(STDERR, " %s (0x%08x)\n", $dt->format("D M j H:i:s Y P"), $t);
		} else
		{
			$this->prt_hex("", substr($p, 1));
		}
	}

	public static function hexstr(string $p) : string
	{
		$len = strlen($p);
		$s = '';
		$hex = "0123456789abcdef";
		for ($i = 0; $i < $len; $i++)
		{
			$c = ord($p[$i]);
			$s .= $hex[($c >> 4) & 0x0f];
			$s .= $hex[$c & 0x0f];
		}
		return $s;
	}

	/*
	 * Return no. of bits in a multiprecision integer.
	 * @param p 	pointer to multiprecision integer
	 * @return		no. of bits
	 */
	private function mpibits(string $p, int $offset) : int
	{
		return ((ord($p[$offset]) << 8) | ord($p[$offset + 1]));
	}

	/*
	 * Return no. of bytes in a multiprecision integer.
	 * @param p 	pointer to multiprecision integer
	 * @return		no. of bytes
	 */
	private function mpilen(string $p, int $offset) : int
	{
		return (2 + (($this->mpibits($p, $offset) + 7) >> 3));
	}
	
	/*
	 * Return hex formatted representation of a multiprecision integer.
	 * @param p 	bytes
	 * @return		hex formatted string (malloc'ed)
	 */
	private function mpistr(string $p, int $offset) : string
	{
		$hex = self::hexstr(substr($p, 2, $this->mpilen($p, $offset) - 2));
		$str = sprintf("[%4u]: %s", $this->grab(substr($p, $offset, 2)), $hex);
		return $str;
	}

	/*
	 * Return value of an OpenPGP string.
	 * @param type		table of (string,value) pairs
	 * @param s 	string token to lookup
	 * @return		byte value
	 */
	private function val_tok(int $type, string $s) : int
	{
		if (isset(self::$valtbl[$type]))
		{
			foreach (self::$valtbl[$type] as $key => $name)
				if ($name == $s)
					return $key;
		}
		return -1;
	}

	/*
	 * Decode length from 1, 2, or 5 octet body length encoding, used in
	 * new format packet headers and V4 signature subpackets.
	 * @param s 	pointer to length encoding buffer
	 * @param slen		buffer size
	 * @retval *lenp	decoded length
	 * @return		no. of bytes used to encode the length, 0 on error
	 */
	private function pgplen(string $s, int &$lenp) : int
	{
		$dlen = 0;
		$lenlen = 0;
		$slen = strlen($s);
		
		/*
		 * Callers can only ensure we'll always have the first byte, beyond
		 * that the required size is not known until we decode it so we need
		 * to check if we have enough bytes to read the size as we go.
		 */
		if (ord($s[0]) < 192)
		{
			$lenlen = 1;
			$dlen = ord($s[0]);
		} else if (ord($s[0]) < 255 && $slen > 2)
		{
			$lenlen = 2;
			$dlen = ((ord($s[0]) - 192) << 8) + ord($s[1]) + 192;
		} else if ($slen > 5)
		{
			$lenlen = 5;
			$dlen = $this->grab(substr($s, 1, 4));
		}

		$lenp = $dlen;

		return $lenlen;
	}

	private function decode_pkt(string $p, array &$pkt) : int
	{
		$rc = -1; /* assume failure */
		$plen = strlen($p);
		
		$pkt = array('tag' => 0, 'blen' => 0);
		/* Valid PGP packet header must always have two or more bytes in it */
		if ($p && $plen >= 2 && (ord($p[0]) & 0x80))
		{
			$lenlen = 0;
			$hlen = 0;
		
			if (ord($p[0]) & 0x40)
			{
				/* New format packet, body length encoding in second byte */
				$lenlen = $this->pgplen(substr($p, 1), $pkt['blen']);
				$pkt['tag'] = (ord($p[0]) & 0x3f);
			} else
			{
				/* Old format packet, body length encoding in tag byte */
				$lenlen = 1 << (ord($p[0]) & 0x3);
				if ($plen > $lenlen)
				{
					$pkt['blen'] = $this->grab(substr($p, 1, $lenlen));
				}
				$pkt['tag'] = (ord($p[0]) >> 2) & 0xf;
			}
			$hlen = $lenlen + 1;
		
			/* Does the packet header and its body fit in our boundaries? */
			if ($lenlen && ($hlen + $pkt['blen'] <= $plen))
			{
				$pkt['head'] = substr($p, 0, $hlen);
				$pkt['body'] = substr($p, $hlen, $pkt['blen']);
				$rc = 0;
			}
		}

		return $rc;
	}

	/*
	 * Return CRC of a buffer.
	 * @param octets	bytes
	 * @return		crc of buffer
	 */
	private function crc24(string $octets) : int
	{
		$crc = 0xb704ce; /* CRC24_INIT */
		$len = strlen($octets);
		
		for ($l = 0; $l < $len; $l++)
		{
			$crc ^= (ord($octets[$l]) & 255) << 16;
			for ($i = 0; $i < 8; $i++)
			{
				$crc <<= 1;
				if ($crc & 0x1000000)
					$crc ^= 0x1864cfb; /* CRC24_POLY */
				$crc &= 0xffffffff;
			}
		}
		return $crc & 0x00ffffff;
	}

	private function base64_crc(string $octets) : string
	{
		$crc = $this->crc24($octets);
		$data = chr(($crc >> 16) & 0xff) . chr(($crc >> 8) & 0xff) . chr($crc & 0xff);
		return base64_encode($data);
	}
	
	private function version(string $h) : int
	{
		if (strlen($h) < 1)
			return -1;

		return ord($h[0]);
	}

	private function prt_subtype(string $h, int $p, int $pend, int $sigtype, array &$digp)
	{
		$plen = 0;
		
		while ($p < $pend)
		{
			$i = $this->pgplen(substr($h, $p, $pend - $p), $plen);
			if ($i == 0 || $plen < 1 || $i + $p + $plen > $pend)
				break;
		
			$p += $i;
		
			$this->prt_val("    ", PGPVAL_SUBTYPE, (ord($h[$p]) & (~PGPSUBTYPE_CRITICAL)));
			if (ord($h[$p]) & PGPSUBTYPE_CRITICAL)
				if ($this->_print)
					if (defined('STDERR'))
						fprintf(STDERR, " *CRITICAL*");
			switch (ord($h[$p]) & ~PGPSUBTYPE_CRITICAL)
			{
			case PGPSUBTYPE_PREFER_SYMKEY:	/* preferred symmetric algorithms */
				for ($i = 1; $i < $plen; $i++)
					$this->prt_val(" ", PGPVAL_SYMKEYALGO, ord($h[$p + $i]));
				break;
			case PGPSUBTYPE_PREFER_HASH:	/* preferred hash algorithms */
				for ($i = 1; $i < $plen; $i++)
					$this->prt_val(" ", PGPVAL_HASHALGO, ord($h[$p + $i]));
				break;
			case PGPSUBTYPE_PREFER_COMPRESS:/* preferred compression algorithms */
				for ($i = 1; $i < $plen; $i++)
					$this->prt_val(" ", PGPVAL_COMPRESSALGO, ord($h[$p + $i]));
				break;
			case PGPSUBTYPE_KEYSERVER_PREFERS:/* key server preferences */
				for ($i = 1; $i < $plen; $i++)
					$this->prt_val(" ", PGPVAL_SERVERPREFS, ord($h[$p + $i]));
				break;
			case PGPSUBTYPE_SIG_CREATE_TIME:
				if (!($digp['saved'] & PGPDIG_SAVED_TIME) &&
					($sigtype == PGPSIGTYPE_POSITIVE_CERT ||
					 $sigtype == PGPSIGTYPE_BINARY ||
					 $sigtype == PGPSIGTYPE_TEXT ||
					 $sigtype == PGPSIGTYPE_STANDALONE))
				{
					if ($plen != (1 + 4)) /* sizeof(uint32_t) */
						break;
					$digp['saved'] |= PGPDIG_SAVED_TIME;
					$digp['time'] = $this->grab(substr($h, $p + 1, 4));
				}
			case PGPSUBTYPE_SIG_EXPIRE_TIME:
			case PGPSUBTYPE_KEY_EXPIRE_TIME:
				$this->prt_time(" ", substr($h, $p + 1, $plen - 1));
				break;
		
			case PGPSUBTYPE_ISSUER_KEYID:	/* issuer key ID */
				if (!($digp['saved'] & PGPDIG_SAVED_ID) &&
					($sigtype == PGPSIGTYPE_POSITIVE_CERT ||
					 $sigtype == PGPSIGTYPE_BINARY ||
					 $sigtype == PGPSIGTYPE_TEXT ||
					 $sigtype == PGPSIGTYPE_STANDALONE))
				{
					if ($plen != (1 + 8))
						break;
					$digp['saved'] |= PGPDIG_SAVED_ID;
					$digp['signid'] = substr($h, $p + 1, 8);
				}
				$this->prt_hex("", substr($h, $p + 1, $plen - 1));
				break;
			case PGPSUBTYPE_EXPORTABLE_CERT:
			case PGPSUBTYPE_TRUST_SIG:
			case PGPSUBTYPE_REGEX:
			case PGPSUBTYPE_REVOCABLE:
			case PGPSUBTYPE_ARR:
			case PGPSUBTYPE_REVOKE_KEY:
			case PGPSUBTYPE_NOTATION:
			case PGPSUBTYPE_PREFER_KEYSERVER:
			case PGPSUBTYPE_PRIMARY_USERID:
			case PGPSUBTYPE_POLICY_URL:
			case PGPSUBTYPE_KEY_FLAGS:
			case PGPSUBTYPE_SIGNER_USERID:
			case PGPSUBTYPE_REVOKE_REASON:
			case PGPSUBTYPE_FEATURES:
			case PGPSUBTYPE_EMBEDDED_SIG:
			case PGPSUBTYPE_ISSUER_FINGERPRINT:
			case PGPSUBTYPE_PREF_AEAD:
			case PGPSUBTYPE_KEY_BLOCK:
			case PGPSUBTYPE_INTERNAL_100:
			case PGPSUBTYPE_INTERNAL_101:
			case PGPSUBTYPE_INTERNAL_102:
			case PGPSUBTYPE_INTERNAL_103:
			case PGPSUBTYPE_INTERNAL_104:
			case PGPSUBTYPE_INTERNAL_105:
			case PGPSUBTYPE_INTERNAL_106:
			case PGPSUBTYPE_INTERNAL_107:
			case PGPSUBTYPE_INTERNAL_108:
			case PGPSUBTYPE_INTERNAL_109:
			case PGPSUBTYPE_INTERNAL_110:
			default:
				$this->prt_hex("", substr($h, $p + 1, $plen - 1));
				break;
			}
			$this->prt_nl();
			$p += $plen;
		}
		return $p != $pend; /* not consuming all bytes is an error */
	}

	private function signature_new(int $algo)
	{
		switch ($algo)
		{
		case PGPPUBKEYALGO_RSA:
			$sa = new PGP_digest_rsa();
			break;
		case PGPPUBKEYALGO_DSA:
			$sa = new PGP_digest_dsa();
			break;
		default:
			$sa = new PGP_digest_null();
			break;
		}
		return $sa;
	}

	private function digest_init(int $algo, int $flags)
	{
		switch ($algo)
		{
		case PGPHASHALGO_MD5:
			$sa = new PGP_digest_md5();
			break;
		case PGPHASHALGO_SHA1:
			$sa = new PGP_digest_sha1();
			break;
		case PGPHASHALGO_SHA256:
			$sa = new PGP_digest_sha256();
			break;
		case PGPHASHALGO_SHA384:
			$sa = new PGP_digest_sha384();
			break;
		case PGPHASHALGO_SHA512:
			$sa = new PGP_digest_sha512();
			break;
		default:
			$sa = null;
			throw new Exception("Unsupported hash algo " . $algo);
			break;
		}
		$sa->flags = $flags;
		return $sa;
	}

	private function prt_sigparams(int $tag, int $pubkey_algo, int $sigtype, int $p, string $h, int $pend, array &$sigp) : int
	{
		$rc = 1; /* assume failure */
		$sigalg = $this->signature_new($pubkey_algo);
		
		for ($i = 0; $i < $sigalg->mpis && $p + 2 <= $pend; $i++)
		{
			$mpil = $this->mpilen($h, $p);
			if ($p + $mpil > $pend)
				break;
			if ($sigtype == PGPSIGTYPE_BINARY || $sigtype == PGPSIGTYPE_TEXT)
			{
				if ($sigalg->setmpi($i, substr($h, $p, $mpil)))
					break;
			}
			$p += $mpil;
		}

		/* Does the size and number of MPI's match our expectations? */
		if ($p == $pend && $i == $sigalg->mpis)
			$rc = 0;
		
		/* We can't handle more than one sig at a time */
		if ($rc == 0 && is_null($sigp['alg']) && $sigp['tag'] == PGPTAG_SIGNATURE)
			$sigp['alg'] = $sigalg;
		else
			unset($sigalg);

		return $rc;
	}

	private function pgpget(string $s, int $offset, int $nbytes, int $send, int &$valp) : int
	{
		$rc = -1;

		if ($nbytes <= $send)
		{
			$valp = $this->grab(substr($s, $offset, $nbytes));
			$rc = 0;
		}

		return $rc;
	}

	private function prt_sig(int $tag, string $h, int $hlen, array &$digp) : int
	{
		$version = 0;
		$rc = 1;

		if (($version = $this->version($h)) < 0)
			return $rc;

		switch ($version)
		{
		case 3:
			/*
			 * 5.2.2. Version 3 Signature Packet Format
			 * 
			 * The body of a version 3 Signature Packet contains:
			 *   - One-octet version number (3).
			 *   - One-octet length of following hashed material.  MUST be 5.
			 *       - One-octet signature type.
			 *       - Four-octet creation time.
			 *   - Eight-octet key ID of signer.
			 *   - One-octet public key algorithm.
			 *   - One-octet hash algorithm.
			 *   - Two-octet field holding left 16 bits of signed hash value.
			 *   - One or more multi-precision integers comprising the signature.
			 *
			 * Algorithm Specific Fields for RSA signatures:
			 *   - multiprecision integer (MPI) of RSA signature value m**d.
			 *
			 * Algorithm Specific Fields for DSA signatures:
			 *   - MPI of DSA value r.
			 *   - MPI of DSA value s.
			struct pgpPktSigV3_s {
				uint8_t version;	 / * version number (3). * /
				uint8_t hashlen;	 / * length of following hashed material. MUST be 5. * /
				uint8_t sigtype;	 / * signature type. * /
				uint8_t time[4];     / * 4 byte creation time. * /
				uint8_t signid[8];   / * key ID of signer. * /
				uint8_t pubkey_algo; / * public key algorithm. * /
				uint8_t hash_algo;	 / * hash algorithm. * /
				uint8_t signhash16[2];	/ * left 16 bits of signed hash value. * /
			};
			 */

			if ($hlen <= 19 || ord($h[1]) != 5)
				return 1;
		
			$sigtype = ord($h[2]);
			$pubkey_algo = ord($h[15]);
			$hash_algo = ord($h[16]);
			$time = substr($h, 3, 4);
			$this->prt_val("V3 ", PGPVAL_TAG, $tag);
			$this->prt_val(" ", PGPVAL_PUBKEYALGO, $pubkey_algo);
			$this->prt_val(" ", PGPVAL_HASHALGO, $hash_algo);
			$this->prt_val(" ", PGPVAL_SIGTYPE, $sigtype);
			$this->prt_nl();
			$this->prt_time(" ", $time);
			$this->prt_nl();
			$this->prt_hex(" signer keyid", substr($h, 7, 8));
			$plen = $this->grab(substr($h, 17, 2));
			$this->prt_hex(" signhash16", substr($h, 17, 2));
			$this->prt_nl();
		
			if ($digp['pubkey_algo'] == 0)
			{
				$digp['version'] = $version;
				$digp['hashlen'] = ord($h[1]);
				$digp['sigtype'] = $sigtype;
				$digp['hash'] = substr($h, 2, $digp['hashlen']);
				$digp['time'] = $this->grab($time);
				$digp['signid'] = substr($h, 7, 8);
				$digp['pubkey_algo'] = $pubkey_algo;
				$digp['hash_algo'] = $hash_algo;
				$digp['signhash16'] = substr($h, 17, 2);
			}
		
			$rc = $this->prt_sigparams($tag, $pubkey_algo, $sigtype, 19, $h, $hlen, $digp);
			break;

		case 4:
			/*
			 * 5.2.3. Version 4 Signature Packet Format
			 * 
			 * The body of a version 4 Signature Packet contains:
			 *   - One-octet version number (4).
			 *   - One-octet signature type.
			 *   - One-octet public key algorithm.
			 *   - One-octet hash algorithm.
			 *   - Two-octet scalar octet count for following hashed subpacket
			 *     data. Note that this is the length in octets of all of the hashed
			 *     subpackets; a pointer incremented by this number will skip over
			 *     the hashed subpackets.
			 *   - Hashed subpacket data. (zero or more subpackets)
			 *   - Two-octet scalar octet count for following unhashed subpacket
			 *     data. Note that this is the length in octets of all of the
			 *     unhashed subpackets; a pointer incremented by this number will
			 *     skip over the unhashed subpackets.
			 *   - Unhashed subpacket data. (zero or more subpackets)
			 *   - Two-octet field holding left 16 bits of signed hash value.
			 *   - One or more multi-precision integers comprising the signature.
			struct pgpPktSigV4_s {
				uint8_t version;	  / * version number (4). * /
				uint8_t sigtype;	  / * signature type. * /
				uint8_t pubkey_algo;  / * public key algorithm. * /
				uint8_t hash_algo;	  / * hash algorithm. * /
				uint8_t hashlen[2];	  / * length of following hashed material. * /
			};
			 */

			if ($hlen <= 6)
				return 1;
		
			$sigtype = ord($h[1]);
			$pubkey_algo = ord($h[2]);
			$hash_algo = ord($h[3]);
			$this->prt_val("V4 ", PGPVAL_TAG, $tag);
			$this->prt_val(" ", PGPVAL_PUBKEYALGO, $pubkey_algo);
			$this->prt_val(" ", PGPVAL_HASHALGO, $hash_algo);
			$this->prt_val(" ", PGPVAL_SIGTYPE, $sigtype);
			$this->prt_nl();
		
			$plen = 0;
			if ($this->pgpget($h, 4, 2, $hlen, $plen))
				return 1;
			$p = 6;
		
			if (($p + $plen) > $hlen)
				return 1;
		
			if ($digp['pubkey_algo'] == 0)
			{
				$digp['hashlen'] = $p + $plen;
				$digp['hash'] = substr($h, 0, $p + $plen);
			}
			if ($this->prt_subtype($h, $p, $p + $plen, $sigtype, $digp))
				return 1;
			$p += $plen;
		
			if ($this->pgpget($h, $p, 2, $hlen, $plen))
				return 1;
			$p += 2;
		
			if (($p + $plen) > $hlen)
				return 1;
		
			if ($this->prt_subtype($h, $p, $p + $plen, $sigtype, $digp))
				return 1;
			$p += $plen;
		
			if ($this->pgpget($h, $p, 2, $hlen, $plen))
				return 1;
			$this->prt_hex(" signhash16", substr($h, $p, 2));
			$this->prt_nl();
		
			if ($digp['pubkey_algo'] == 0)
			{
				$digp['version'] = $version;
				$digp['sigtype'] = $sigtype;
				$digp['pubkey_algo'] = $pubkey_algo;
				$digp['hash_algo'] = $hash_algo;
				$digp['signhash16'] = substr($h, $p, 2);
			}
		
			$p += 2;
			if ($p > $hlen)
				return 1;
		
			$rc = $this->prt_sigparams($tag, $pubkey_algo, $sigtype, $p, $h, $hlen, $digp);
			break;

		default:
			trigger_error("Unsupported version of key: V" . $version, E_USER_WARNING);
			break;
		}
		return $rc;
	}

	private function pubkey_new(int $algo)
	{
		switch ($algo)
		{
		case PGPPUBKEYALGO_RSA:
			$sa = new PGP_pubkey_rsa();
			break;
		case PGPPUBKEYALGO_DSA:
			$sa = new PGP_pubkey_dsa();
			break;
		default:
			$sa = new PGP_pubkey_null();
			break;
		}
		return $sa;
	}

	private function prt_pubkeyparams(int $pubkey_algo, int $p, string $h, int $pend, array &$keyp) : int
	{
		$rc = 1;
		$keyalg = $this->pubkey_new($pubkey_algo);

		for ($i = 0; $i < $keyalg->mpis && $p + 2 <= $pend; $i++)
		{
			$mpil = $this->mpilen($h, $p);
			if ($p + $mpil > $pend)
				break;
			if ($keyalg->setmpi($i, substr($h, $p, $mpil)))
				break;
			$p += $mpil;
		}

		/* Does the size and number of MPI's match our expectations? */
		if ($p == $pend && $i == $keyalg->mpis)
			$rc = 0;

		/* We can't handle more than one key at a time */
		if ($rc == 0 && is_null($keyp['alg']) &&
			($keyp['tag'] == PGPTAG_PUBLIC_KEY || $keyp['tag'] == PGPTAG_PUBLIC_SUBKEY))
			$keyp['alg'] = $keyalg;
		else
			unset($keyalg);

		return $rc;
	}

	private function prt_key(int $tag, string $h, int $hlen, array &$digp) : int
	{
		$version = 0;
		$rc = 1;

		if (($version = $this->version($h)) < 0)
			return $rc;

		/* We only permit V4 keys, V3 keys are long long since deprecated */
		switch ($version)
		{
		case 4:
			/*
			 * The version 4 format is similar to the version 3 format except for
			 * the absence of a validity period.  This has been moved to the
			 * signature packet.  In addition, fingerprints of version 4 keys are
			 * calculated differently from version 3 keys, as described in section
			 * "Enhanced Key Formats."
			 *
			 * A version 4 packet contains:
			 *   - A one-octet version number (4).
			 *   - A four-octet number denoting the time that the key was created.
			 *   - A one-octet number denoting the public key algorithm of this key
			 *   - A series of multi-precision integers comprising the key
			 *     material.  This algorithm-specific portion is:
			 *
			 *     Algorithm Specific Fields for RSA public keys:
			 *       - multiprecision integer (MPI) of RSA public modulus n;
			 *       - MPI of RSA public encryption exponent e.
			 *
			 *     Algorithm Specific Fields for DSA public keys:
			 *       - MPI of DSA prime p;
			 *       - MPI of DSA group order q (q is a prime divisor of p-1);
			 *       - MPI of DSA group generator g;
			 *       - MPI of DSA public key value y (= g**x where x is secret).
			 *
			 *     Algorithm Specific Fields for Elgamal public keys:
			 *       - MPI of Elgamal prime p;
			 *       - MPI of Elgamal group generator g;
			 *       - MPI of Elgamal public key value y (= g**x where x is
			 *         secret).
			 *
			struct pgpPktKeyV4_s {
				uint8_t version;		/ * version number (4). * /
				uint8_t time[4];		/ * time that the key was created. * /
				uint8_t pubkey_algo;	/ * public key algorithm. * /
			};
			 */
			if ($hlen > 6)
			{
				$pubkey_algo = ord($h[5]);
				$time = substr($h, 1, 4);
				$this->prt_val("V4 ", PGPVAL_TAG, $tag);
				$this->prt_val(" ", PGPVAL_PUBKEYALGO, $pubkey_algo);
				$this->prt_time(" ", $time);
				$this->prt_nl();
		
				/* If _digp->hash is not NULL then signature is already loaded */
				if (is_null($digp['hash']))
				{
					$digp['version'] = $version;
					$digp['time'] = $this->grab($time);
					$digp['pubkey_algo'] = $pubkey_algo;
				}
		
				$rc = $this->prt_pubkeyparams($pubkey_algo, 6, $h, $hlen, $digp);
			}
			break;
		default:
			trigger_error("Unsupported version of key: V" . $version, E_USER_WARNING);
			break;
		}
		return $rc;
	}

	private function prt_userid(int $tag, string $body, int $blen, array &$digp) : int
	{
		$this->prt_val("", PGPVAL_TAG, $tag);
		if ($this->_print)
			if (defined('STDERR'))
				fprintf(STDERR, " \"%s\"", $body);
		$this->prt_nl();
		$digp['userid'] = substr($body, 0, $blen);
		return 0;
	}

	private function pubkey_fingerprint(string $h, int $hlen, string &$fp) : int
	{
		$rc = -1; /* assume failure */

		if (($version = $this->version($h)) < 0)
			return $rc;

		/* We only permit V4 keys, V3 keys are long long since deprecated */
		switch ($version)
		{
		case 4:
			$mpis = -1;
		
			/* Packet must be larger than v to have room for the required MPIs */
			if ($hlen > 6)
			{
				$pubkey_algo = ord($h[5]);
				$sa = $this->pubkey_new($pubkey_algo);
				$mpis = $sa->mpis;
				unset($sa);
			}
		
			$se = 6;
			while ($se < $hlen && $mpis-- > 0)
				$se += $this->mpilen($h, $se);
		
			/* Does the size and number of MPI's match our expectations? */
			if ($se == $hlen && $mpis == 0)
			{
				$ctx = $this->digest_init(PGPHASHALGO_SHA1, PGPDIGEST_NONE);
				$i = $se;
				$in = '\x99' . chr($i >> 8) . chr($i & 0xff);
		
				$ctx->update($in, 3);
				$ctx->update($h, $i);
				$d = $ctx->final(0);
		
				if (strlen($d) == $ctx->digestlen)
				{
					$rc = 0;
					$fp = $d;
				} else
				{
					unset($d);
				}
			}
			break;

		default:
			trigger_error("Unsupported version of key: V" . $version, E_USER_WARNING);
			break;
		}
		return $rc;
	}

	private function get_keyid(string $h, int $hlen, string &$keyid) : int
	{
		$fp = '';
		$rc = $this->pubkey_fingerprint($h, $hlen, $fp);
		if ($rc == 0 && strlen($fp) > 8)
		{
			$keyid = substr($fp, -8);
			unset($fp);
		}
		return $rc;
	}

	private function pubkey_keyid(string $pkt, string &$keyid) : int
	{
		$p = array();
		if ($this->decode_pkt($pkt, $p))
			return -1;
		
		return $this->get_keyid($p['body'], $p['blen'], $keyid);
	}

	private function prt_pkt(array &$pkt, array &$digp) : int
	{
		$rc = 0;
	
		switch ($pkt['tag'])
		{
		case PGPTAG_SIGNATURE:
			$rc = $this->prt_sig($pkt['tag'], $pkt['body'], $pkt['blen'], $digp);
			break;
		case PGPTAG_PUBLIC_KEY:
			/* Get the public key Key ID. */
			if (!$this->get_keyid($pkt['body'], $pkt['body'], $digp['signid']))
				$digp['saved'] |= PGPDIG_SAVED_ID;
			else
				$digp['signid'] = "";
			$rc = $this->prt_key($pkt['tag'], $pkt['body'], $pkt['blen'], $digp);
			break;
		case PGPTAG_USER_ID:
			$rc = $this->prt_userid($pkt['tag'], $pkt['body'], $pkt['blen'], $digp);
			break;
		case PGPTAG_RESERVED:
			$rc = -1;
			break;
		case PGPTAG_COMMENT:
		case PGPTAG_COMMENT_OLD:
		case PGPTAG_PUBLIC_SUBKEY:
		case PGPTAG_SECRET_KEY:
		case PGPTAG_SECRET_SUBKEY:
		case PGPTAG_PUBLIC_SESSION_KEY:
		case PGPTAG_SYMMETRIC_SESSION_KEY:
		case PGPTAG_COMPRESSED_DATA:
		case PGPTAG_SYMMETRIC_DATA:
		case PGPTAG_MARKER:
		case PGPTAG_LITERAL_DATA:
		case PGPTAG_TRUST:
		case PGPTAG_PHOTOID:
		case PGPTAG_ENCRYPTED_MDC:
		case PGPTAG_MDC:
		case PGPTAG_ENCRYPTED_AEAD:
		case PGPTAG_PRIVATE_60:
		case PGPTAG_PRIVATE_62:
		case PGPTAG_CONTROL:
		default:
			$this->prt_val("", PGPVAL_TAG, $pkt['tag']);
			$this->prt_hex("", $pkt['body']);
			$this->prt_nl();
			break;
		}
	
		return $rc;
	}

	public function prt_params(int $pkttype, array &$ret) : int
	{
		$this->_print = 1;
		$pkts = $this->data;
		$pend = $this->datalen;
		$digp = array(
			'userid' => '',
			'hash' => null,
			'tag' => 0,
			'version' => 0,
			'time' => time(),
			'pubkey_algo' => 0,
			'hash_algo' => 0,
			'hashlen' => 0,
			'signhash16' => '',
			'signid' => '',
			'saved' => 0,
			'alg' => null,
		);
		$first = true;
		$pkt = array();
		$rc = -1; /* assume failure */
	
		$p = 0;
		while ($p < $pend)
		{
			if ($this->decode_pkt(substr($pkts, $p), $pkt))
				break;
		
			if ($first)
			{
				if ($pkttype && $pkt['tag'] != $pkttype)
				{
					break;
				} else
				{
					$digp['tag'] = $pkt['tag'];
					$first = false;
				}
			}

			if ($this->prt_pkt($pkt, $digp))
				break;

			$p += strlen($pkt['head']) + $pkt['blen'];
		}

		$rc = (!$first && ($p == $pend)) ? 0 : -1;

		if ($rc == 0)
		{
			$ret = $digp;
		} else
		{
			unset($digp);
		}
		return $rc;
	}

	public function prt_pkts(array &$dig, int $printing) : int
	{
		$digp = array();
	
		$this->_print = $printing;
	
		$rc = $this->prt_params(0, $digp);
	
		if ($rc == 0)
		{
			if ($digp['tag'] == PGPTAG_SIGNATURE)
			{
				$dig['signature'] = $digp;
			} else
			{
				$dig['pubkey'] = $digp;
			}
		} else
		{
			unset($digp);
		}

		$this->_print = false;
		return $rc;
	}

	public function ident_item(array &$digp) : string
	{
		if (isset($digp['version']))
		{
			$signid = self::hexstr(substr($digp['signid'], 4));
			$id = sprintf("V%d %s/%s %s, key ID %s",
				$digp['version'],
				$this->val_string(PGPVAL_PUBKEYALGO, $digp['pubkey_algo']),
				$this->val_string(PGPVAL_HASHALGO, $digp['hash_algo']),
				$this->val_string(PGPVAL_TAG, $digp['tag']),
				$signid);
		} else
		{
			$id = "(none)";
		}
		return $id;
	}

	private function decode_pkts(string $b, string &$pkt) : int
	{
		$crcenc = 0;
		$pstate = 0;
		$armortype = null;
		$enc = 0;
		
		$blen = strlen($b);
		for ($t = 0; $t < $blen; $t = $te)
		{
			if (($te = strpos($b, '\n', $t)) === false)
				$te = $blen;
			else
				$te++;
		
			switch ($pstate)
			{
			case 0:
				if (substr($b, $t, 15) != "-----BEGIN PGP ")
					continue 2;
				$t += 15;
		
				$rc = $this->val_tok(PGPVAL_ARMORBLOCK, substr($b, $t, $te - $t));
				if ($rc < 0)
				{
					return PGPARMOR_ERR_UNKNOWN_ARMOR_TYPE;
				}
				if ($rc != PGPARMOR_PUBKEY)	/* ASCII Pubkeys only, please. */
					continue 2;
		
				$armortype = $this->val_string(PGPVAL_ARMORBLOCK, $rc);
				$t += strlen($armortype);
				if (substr($b, $t, 5) != "-----")
					continue 2;
				$t += 5;
				if ($b[$t] != "\n" && $b[$t] != "\r")
					continue 2;
				$pstate++;
				break;
			case 1:
				$enc = 0;
				$rc = $this->val_tok(PGPVAL_ARMORKEY, substr($b, $t, $te - $t));
				if ($rc >= 0)
					continue 2;
				if ($b[$t] != "\n" && $b[$t] != "\r")
				{
					$pstate = 0;
					continue 2;
				}
				$enc = $te;		/* Start of encoded packets */
				$pstate++;
				break;
			case 2:
				$crcenc = 0;
				if ($b[$t] != '=')
					continue 2;
				$t++;	/* Terminate encoded packets */
				$crcenc = $t; 	/* Start of encoded crc */
				$pstate++;
				break;
			case 3:
				$pstate = 0;
				if (substr($b, $t, 13) != "-----END PGP ")
				{
					return PGPARMOR_ERR_NO_END_PGP;
				}
				// $t = 0;		/* Terminate encoded crc */
				$t += 13;
				if ($t >= $te)
					continue 2;
		
				if (is_null($armortype)) /* can't happen */
					continue 2;
				if (substr($b, $t, strlen($armortype)) != $armortype)
					continue 2;
		
				$t += strlen($armortype);
				if ($t >= $te)
					continue 2;
		
				if (substr($b, $t, 5) != "-----")
				{
					return PGPARMOR_ERR_NO_END_PGP;
				}
				$t += 5;
				/* Handle EOF without EOL here, *t == '\0' at EOF */
				if ($t >= $te)
					continue 2;
				/* permitting \r here is not RFC-2440 compliant <shrug> */
				if (!($b[$t] == "\n" || $b[$t] == "\r" || $t == $blen))
					continue 2;
		
				$crcdec = base64_decode(substr($b, $crcenc), true);
				if ($crcdec === false)
				{
					return PGPARMOR_ERR_CRC_DECODE;
				}
				$crcpkt = $this->grab($crcdec);
				unset($crcdec);
				$dec = base64_decode(substr($b, $enc), true);
				if ($dec === false)
				{
					return PGPARMOR_ERR_BODY_DECODE;
				}
				$crc = $this->crc24($dec);
				if ($crcpkt != $crc)
				{
					return PGPARMOR_ERR_CRC_CHECK;
				}
				$pkt = $dec;
				return PGPARMOR_PUBKEY;	/* ASCII Pubkeys only, please. */
			}
		}
		return PGPARMOR_NONE;
	}

	public function parse_pkts(string $b, string &$pkt) : int
	{
		return $this->decode_pkts($b, $pkt);
	}

	public function pubkey_certlen(int &$certlen) : int
	{
		$pkts = $this->data;
		$pktslen = $this->datalen;
		$pend = $pktslen;
	
		$pkt = array('tag' => 0, 'blen' => 0);
		$p = 0;
		while ($p < $pend)
		{
			if ($this->decode_pkt(substr($pkts, $p), $pkt))
				return -1;
		
			if ($pkt['tag'] == PGPTAG_PUBLIC_KEY && $p != 0)
			{
				$certlen = $p;
				return 0;
			}
		
			$p += strlen($pkt['head']) + $pkt['blen'];
		}
	
		$certlen = $pktslen;
	
		return 0;
	}

	public function armor_wrap(int $atype, string $s)
	{
		$enc = base64_encode($s);
		$crc = $this->base64_crc($s);
		$valstr = $this->val_string(PGPVAL_ARMORBLOCK, $atype);
	
		$buf = '';
		if ($crc != '' && $enc != '')
		{
			$buf = sprintf("%s=%s", $enc, $crc);
		}

		$val = sprintf("-----BEGIN PGP %s-----\nVersion: php-%s (OpenSSL)\n\n%s\n-----END PGP %s-----\n",
			$valstr, phpversion(), $buf, $valstr);

		return $val;
	}

}

?>

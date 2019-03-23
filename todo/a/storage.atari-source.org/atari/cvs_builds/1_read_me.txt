Hello community!

This folder houses archives of CVS builds of the MiNT kernel and at times
MiNTLib.  I originally promised daily but it seems to happen pretty much
weekly.  If anything changes, the scripts need modified.  Please
let me know if files are missing from the archives!

The script has been modified so that if the build fails, I'll know and bogus
archives won't be uploaded.

So here's the files:
The prefix is the date in the form of YYYY.mm.dd.

The next part is either the freemint kernel
or the mint library (libc for MiNT).

The last part can be either bin or cmpsrc.
bin stands for a normal binary distribution of this package.
cmpsrc stands for the source directory with the source distribution as it 
would come from CVS except it's precompiled for you.  You can do make 
install, etc.

The final piece is either .tar.gz or .zip, which simply is the archive 
format provided in both for your convenience.

If you have any questions about these builds please email the MiNT mailing 
list, or contact me directly at mducksub and that's at atari-source.com.  
Sorry for the spam proofing, hope you can figure it out.

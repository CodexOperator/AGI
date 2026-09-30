# ram-write.sh -- THE one RAM-write rule of the guard scripts (SOURCED by both
# ram-main.sh and session-sweep.sh, which used to carry it byte-identically): a
# write whose DESTINATION is on the tmpfs is charged to the ramdisk.slice
# through mem_cap.py's shell entry, which asks the FILESYSTEM (--to), never a
# path prefix -- the RAM tree is an rbind overmount AT MAIN, so "$RAM_DIR"/*
# never names it (hypothesis:g7556-...).
ramw() { local p=$1; shift; python3 "$HERE/../bin/mem_cap.py" ram-exec --to "$p" -- "$@"; }

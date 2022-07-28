import subprocess, os, argparse, shutil
import plot_result as pr

L1D_cache_sizes = ['16K', '32K', '64K', '128K']
LL_cache_sizes = ['2M', '4M', '8M', '16M', '32M']
run_args = ['-t', 'drcachesim', '-indir']
processes_dict = {} 
outdir_dict = {}

parser = argparse.ArgumentParser(description='Run drcachesim on trace with different cache sizes.')
parser.add_argument('indirs', nargs='+',
                    help='input directories containing traces')
parser.add_argument('-o', '--outdirs', nargs='+', help='output directories')
parser.add_argument('--LL-cache-sizes', nargs='+', dest='LL_cache_sizes',
                    default=LL_cache_sizes,
                    help='specify LL cache sizes (default: [2M, 4M, 8M, 16M, 32M])')
parser.add_argument('--drrun-bin', dest='bin', default='dynamorio/bin64/drrun', help='path to drrun binary')
parser.add_argument('--remove-saved-results', dest='remove_saved_results', action='store_true', help='remove saved results')
parser.add_argument('--rerun-sim', dest='rerun_sim', action='store_true', help='Rerun simulation')
args = parser.parse_args()

if args.outdirs is not None and len(args.outdirs) != len(args.indirs):
    print('Number of output directories must match number of input directories')
    exit(1)

for i, indir in enumerate(args.indirs):
    if args.outdirs is None:
        base = os.path.basename(indir)
        if base == "":
            base  = os.path.basename(os.path.split(indir)[0])
        outdir = base + '_results'
    else:
        outdir = args.outdirs[i]
    outdir_dict[indir] = outdir
    if args.remove_saved_results:
        shutil.rmtree(outdir, ignore_errors=True)
    if not os.path.exists(outdir):
        os.makedirs(outdir)


for s in args.LL_cache_sizes:
    for indir in args.indirs:
        if os.path.isfile(outdir_dict[indir] + "/LL_size_" + s + ".txt") and not args.rerun_sim:
            continue
        p = subprocess.Popen([args.bin] + run_args + [indir, '-LL_size', s], stderr=subprocess.PIPE)
        processes_dict[p] = (outdir_dict[indir], s)

for kvp in processes_dict.items():
    p = kvp[0]
    outdir = kvp[1][0]
    size = kvp[1][1]
    err = p.communicate()[1];
    with open(outdir + "/LL_size_" + size + ".txt", "w") as f: 
        f.write(err.decode())

pr.plot_result(outdir_dict.values())

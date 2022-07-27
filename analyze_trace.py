import subprocess, os, argparse, shutil
import plot_result as pr

L1D_cache_sizes = ['16K', '32K', '64K', '128K']
LL_cache_sizes = ['2M', '4M', '8M', '16M', '32M']
run_args = ['-t', 'drcachesim', '-indir']
processes = [] 
outdir_dict = {}

parser = argparse.ArgumentParser(description='Run drcachesim on trace with different cache sizes.')
parser.add_argument('indirs', nargs='+',
                    help='input directories containing traces')
parser.add_argument('--LL_cache_sizes', nargs='+', dest='LL_cache_sizes',
                    default=LL_cache_sizes,
                    help='specify LL cache sizes (default: [2M, 4M, 8M, 16M, 32M])')
parser.add_argument('--drrun_bin', dest='bin', default='dynamorio/bin64/drrun', help='path to drrun binary')
parser.add_argument('--remove_cached_results', dest='remove_cached_results', action='store_true', help='remove cached results')
parser.add_argument('--rerun_sim', dest='rerun_sim', action='store_true', help='Rerun simulation')
args = parser.parse_args()

for indir in args.indirs:
    base = os.path.basename(indir)
    if base == "":
        base  = os.path.basename(os.path.split(indir)[0])
    outdir = base + '_results'
    outdir_dict[indir] = outdir
    if args.remove_cached_results:
        shutil.rmtree(outdir, ignore_errors=True)
    if not os.path.exists(outdir):
        os.makedirs(outdir)


for s in args.LL_cache_sizes:
    for indir in args.indirs:
        if outdir_dict[indir] in os.listdir(indir) and not args.rerun_sim:
            continue
        processes.append(subprocess.Popen([args.bin] + run_args + [indir, '-LL_size', s], stderr=subprocess.PIPE))

for p in processes:
    err = p.communicate()[1];
    with open(outdir_dict[p.args[4]] + "/LL_size_" + p.args[-1] + ".txt", "w") as f: 
        f.write(err.decode())

pr.plot_result(outdir_dict.values())

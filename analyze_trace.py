from re import T
import subprocess, os, argparse
import plot_result as pr

L1D_cache_sizes = ['16K', '32K', '64K', '128K']
LL_cache_sizes = ['2M', '4M', '8M', '16M', '32M']
run_args = ['dynamorio/bin64/drrun', '-t', 'drcachesim', '-indir']
processes = [] 
outdir_dict = {}

parser = argparse.ArgumentParser(description='Run drcachesim on trace with different cache sizes.')
parser.add_argument('indirs', nargs='+',
                    help='input directories containing traces')
parser.add_argument('--LL_cache_sizes', nargs='+', dest='LL_cache_sizes',
                    default=LL_cache_sizes,
                    help='specify LL cache sizes (default: [2M, 4M, 8M, 16M, 32M])')

args = parser.parse_args()

cached = True 
for indir in args.indirs:
    outdir = os.path.basename(indir) + '_results'
    outdir_dict[indir] = outdir

    if not os.path.exists(outdir):
        os.makedirs(outdir)
        cached = False
if cached:
    pr.plot_result(outdir_dict.values())
    exit(0)

for s in args.LL_cache_sizes:
    for indir in args.indirs:
        processes.append(subprocess.Popen(run_args + [indir, '-LL_size', s], stderr=subprocess.PIPE))

for p in processes:
    err = p.communicate()[1];
    with open(outdir_dict[p.args[4]] + "/LL_size_" + p.args[-1] + ".txt", "w") as f: 
        f.write(err.decode())

pr.plot_result(outdir_dict.values())

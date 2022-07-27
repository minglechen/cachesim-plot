import matplotlib.pyplot as plt, os, numpy as np

def convert_prefix(prefix):
    if prefix == 'K':
        return 1024
    elif prefix == 'M':
        return 1024**2
    elif prefix == 'G':
        return 1024**3
    else:
        return 1

def plot_result_internal(outdir):
    files = os.listdir(outdir)
    run_name = os.path.basename(outdir).split('_')[0]
    cache_sizes = np.array([])
    miss_rates = np.array([])
    for file in files:
        if file.startswith('LL_size_') and file.endswith('.txt'):
            cache_size = file[8:-4]
            with open(os.path.join(outdir, file), 'r') as f:
                buf = f.read()
                ind = buf.find('Local miss rate:')
                if ind == -1:
                    continue
                else:
                    ind += len('Local miss rate:')
                    miss_rate = float(buf[ind:].split()[0].strip('%'))/100
                    cache_sizes = np.append(cache_sizes, cache_size)
                    miss_rates = np.append(miss_rates, miss_rate)

    cache_sizes_bytes = np.array([int(x[:-1])*convert_prefix(x[-1]) for x in cache_sizes])
    ind = np.argsort(cache_sizes_bytes)
    cache_sizes_bytes = cache_sizes_bytes[ind]
    miss_rates = miss_rates[ind]
    cache_sizes = cache_sizes[ind]

    plt.plot(cache_sizes_bytes, miss_rates, 'o-', label=run_name)
    plt.xticks(cache_sizes_bytes, cache_sizes)

def plot_result(outdirs):
    for outdir in outdirs:
        plot_result_internal(outdir)
    plt.xlabel('LL cache size')
    plt.ylabel('Local miss rate')
    # plt.ylim(0, 1)
    plt.title('Local miss rate vs LL cache size')
    plt.legend(loc='upper right')
    plt.show()

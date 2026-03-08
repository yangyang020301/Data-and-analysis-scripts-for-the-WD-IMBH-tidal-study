# Load necessary packages
import numpy as np
import matplotlib.pyplot as plt
from few.utils.utility import get_mismatch
from tqdm import tqdm
import glob
import os
from joblib import Parallel, delayed
import warnings
import cmocean
warnings.filterwarnings('ignore', category=UserWarning)

# Set up the plot style
plt.rcParams['text.usetex'] = False
plt.rcParams['mathtext.rm'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.family'] = 'serif'

# Get list of data files
data_files = sorted(glob.glob('data_files/pro/EMRI_TH_GW_Waveform_M_1e5_mu_6e-1_rp_*_6mons_a=0p9.npz'))

# Extract rp values and sort
rps_files = []
for f in data_files:
    try:
        # Extract the number after 'rp_' and before '_6mons'
        rp_val = int(f.split('rp_')[1].split('_')[0])
        rps_files.append((rp_val, f))
    except:
        continue

# Sort by rp
rps_files.sort(key=lambda x: x[0], reverse=True)

# Function to process a single file WITHOUT tqdm (to avoid pickling issues)
def process_file_no_tqdm(rp, file_path, downsample_factor=8):
    """
    Process a single file and compute mismatch over time.
    
    Parameters:
    -----------
    rp : int
        Pericenter radius value
    file_path : str
        Path to the data file
    downsample_factor : int
        Factor by which to downsample the waveforms
        
    Returns:
    --------
    tuple : (rp, time_array, mismatch_array)
    """
    try:
        # Load data
        data = np.load(file_path, allow_pickle=True)
        h_GW = data['h_GW']
        h_TH = data['h_TH']
        
        # Downsample for efficiency
        h_GW = h_GW[::downsample_factor]
        h_TH = h_TH[::downsample_factor]
        
        # Compute mismatch over time WITHOUT tqdm
        mismatch = []
        for i in tqdm(range(1, len(h_GW))):
            MM = get_mismatch(h_GW[:i], h_TH[:i])
            mismatch.append(MM)
        
        # Create time array (6 months total)
        time = np.linspace(0, 182.5, len(mismatch))
        
        return rp, time, mismatch
        
    except Exception as e:
        print(f"Error processing rp={rp} from {file_path}: {e}")
        return rp, None, None

# Alternative: Use a simpler progress tracking approach
print(f"Processing {len(rps_files)} files...")
print("-" * 50)

# Track progress manually
results = []
processed_count = 0

# Process in smaller batches to show progress
batch_size = 20#min(2, len(rps_files))  # Smaller batches for better progress feedback

for i in range(0, len(rps_files), batch_size):
    batch = rps_files[i:i+batch_size]
    batch_num = i // batch_size + 1
    total_batches = (len(rps_files) + batch_size - 1) // batch_size
    
    print(f"\nProcessing batch {batch_num}/{total_batches} (files {i+1}-{min(i+batch_size, len(rps_files))})")
    
    # Process this batch in parallel
    batch_results = Parallel(n_jobs=batch_size)(
        delayed(process_file_no_tqdm)(rp, file_path) for rp, file_path in batch
    )
    
    results.extend(batch_results)
    processed_count += len(batch)
    
    # Show progress
    print(f"✓ Completed {processed_count}/{len(rps_files)} files")
    
    # Show individual file progress within batch
    for (rp, file_path), (result_rp, time, mismatch) in zip(batch, batch_results):
        if time is not None and mismatch is not None:
            print(f"  rp={rp}: ✓ Success ({len(mismatch)} points)")
        else:
            print(f"  rp={rp}: ✗ Failed")

print("-" * 50)

# Filter out failed results
valid_results = []
failed_results = []
for rp, time, mismatch in results:
    if time is not None and mismatch is not None:
        valid_results.append((rp, time, mismatch))
    else:
        failed_results.append(rp)

print(f"Successfully processed {len(valid_results)} out of {len(rps_files)} files")
if failed_results:
    print(f"Failed to process files with rp: {failed_results}")

# Sort by rp for consistent coloring
valid_results.sort(key=lambda x: x[0], reverse=True)
# Create colormap
rps = [rp for rp, _, _ in valid_results]
cmap = cmocean.cm.balance  # or viridis, summer, winter, etc.
norm = plt.Normalize(min(rps), max(rps))


# Create figure with explicit axis
plt.rc('xtick', labelsize=25)   # fontsize of the tick labels
plt.rc('ytick', labelsize=25)   # fontsize of the tick labels
fig = plt.figure(figsize=(13, 10))
ax = fig.add_subplot(111)  # Create a single subplot

# Plot results with tqdm for plotting progress
print("\nPlotting results...")
for idx, (rp, time, mismatch) in enumerate(tqdm(valid_results, desc="Plotting waveforms", unit="waveform")):
    color = cmap(norm(rp))
    
    # ALWAYS add label for EVERY curve to show all in legend
    ax.loglog(time, mismatch, '-', color=color, alpha=0.8, 
               linewidth=1.5, label=fr'${rp}M_\bullet$')

# Add colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
#cbar = fig.colorbar(sm, ax=ax, pad=0.02)  # Use fig.colorbar with ax parameter
#cbar.set_label(r'Pericenter Radius $r_p\,[M]$', fontsize=14)
#cbar.ax.tick_params(labelsize=12)

# Final plot formatting
ax.set_xlabel(r'$t$ [days]', fontsize=30)
ax.set_ylabel(r'$1-\mathcal{M}$', fontsize=30)
#ax.set_title('Waveform Mismatch for Different Pericenter Radii', fontsize=16)
ax.set_xlim(1e-1,182.5)
ax.set_ylim(1e-11,10)
ax.grid(color='black', linestyle=':', alpha=0.5)
ax.legend(framealpha=1, fontsize=22, loc='upper center', ncols=5, bbox_to_anchor=(0.5, 1.17))
fig.tight_layout()

print("\nPlot completed successfully!")
fig.savefig('mismatch_vs_time_rp_colormap_spin.png', dpi=300, bbox_inches='tight')
fig.savefig('mismatch_vs_time_rp_colormap_spin.pdf', dpi=300, bbox_inches='tight')
plt.show()
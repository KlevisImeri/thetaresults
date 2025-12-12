import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# --- Configuration ---
# Set the backend to 'Agg' to prevent matplotlib from opening a GUI window.
matplotlib.use('Agg')

# Path to your data file.
CSV_FILE_PATH = './results/4:PredCart(900, true, true) -> KInd() | 4:PredCart(900, true) -> KInd() | 4:PredCart(100, true, true) -> KInd() | 3:PredCart(100, true) -> KInd() | 3:PredCart(100, pRes=false) -> KInd() | 4:PredCart() | 1:Kind()/results.2025-11-02_14-20-04.table.csv'


def generate_quantile_plot_pdf(csv_path):
    """
    Parses a BenchExec results file, refactors configuration names, and
    generates an extra-large plot with an adjusted smaller title and larger legend.

    Args:
        csv_path (str): The file path to the CSV/TSV results.
    """
    try:
        df = pd.read_csv(csv_path, header=[0, 1, 2], index_col=0, sep='\t')
    except FileNotFoundError:
        print(f"Error: The file '{csv_path}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    df.columns = df.columns.set_levels(df.columns.levels[1].str.replace(r'\.SV-COMP25_unreach-call$', '', regex=True), level=1)
    run_sets = df.columns.get_level_values('run set').unique()

    # --- Plotting ---
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Using the large figure size
    plt.figure(figsize=(18, 12))

    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd',
        '#8c564b', '#e377c2', '#d62728'
    ]
    
    print("Processing configurations...")
    
    plot_index = 0
    for run_set in run_sets:
        if 'pRes=false' in run_set:
            print(f"Skipping configuration: {run_set}")
            continue

        label = run_set
        if label == 'KInd()':
            label = 'KInd(900)'
        if label == 'PredCart()':
            label = 'PredCart(900)'

        label = label.replace(', true, true)', ', pRes, Heu)')
        label = label.replace(', true)', ', pRes)')
        
        run_set_df = df.xs(run_set, level='run set', axis=1)
        try:
            status_col = run_set_df.columns[run_set_df.columns.get_level_values(1) == 'status'][0]
            cputime_col = run_set_df.columns[run_set_df.columns.get_level_values(1) == 'cputime (s)'][0]
        except IndexError:
            print(f"Warning: Columns 'status' or 'cputime (s)' not found for '{run_set}'. Skipping.")
            continue
            
        correct_mask = (run_set_df[status_col] == 'true') | (run_set_df[status_col].astype(str).str.startswith('false('))
        correct_times = run_set_df.loc[correct_mask, cputime_col]
        cputime_numeric = pd.to_numeric(correct_times, errors='coerce').dropna().sort_values()

        if cputime_numeric.empty:
            print(f"No correct results with valid cputime for: {run_set}")
            continue

        print(f"Plotting with label: '{label}' ({len(cputime_numeric)} correct results)")

        y_values = cputime_numeric.values
        x_values = np.arange(1, len(y_values) + 1)

        # Using the thick lines and large markers
        plt.plot(x_values, y_values, marker='o', linestyle='-', 
                 markersize=6,
                 linewidth=3,
                 label=label, 
                 color=colors[plot_index % len(colors)])
        plot_index += 1

    # --- Final Plot Customization ---
    plt.yscale('log')
    plt.xlabel('Number of Solved Tasks', fontsize=24)
    plt.ylabel('CPU Time (s) [log scale]', fontsize=24)
    
    # --- CHANGE 1: Make the title smaller ---
    plt.title('CPU Time Quantile Plot', fontsize=22, fontweight='bold') # Previously 28

    plt.tick_params(axis='both', which='major', labelsize=18)

    # --- CHANGE 2: Make the legend larger ---
    plt.legend(title='Configurations', loc='upper left', 
               fontsize=20,       # Previously 18
               title_fontsize=22) # Previously 20
    
    plt.grid(True, which="both", ls=":", linewidth=0.9, color='darkgray')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    try:
        # --- CHANGE 3: Update output filename ---
        output_filename = "cputime_quantile_plot_adjusted.pdf"
        plt.savefig(output_filename, bbox_inches='tight', dpi=300)
        print(f"\nPlot successfully saved as '{output_filename}'")
    except Exception as e:
        print(f"\nAn error occurred while saving the PDF: {e}")

# Run the function when the script is executed.
if __name__ == '__main__':
    generate_quantile_plot_pdf(CSV_FILE_PATH)

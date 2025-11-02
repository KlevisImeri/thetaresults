import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# --- Configuration ---
# Set the backend to 'Agg' to prevent matplotlib from opening a GUI window.
matplotlib.use('Agg')

# Path to your data file.
CSV_FILE_PATH = './results/4:PredCart(900, true, true) -> KInd() | 4:PredCart(900, true) -> KInd() | 4:PredCart() | 1:Kind()/results.2025-11-02_01-36-41.table.csv' # Replace with the path to your CSV file


def generate_quantile_plot_pdf(csv_path):
    """
    Parses a BenchExec results file and generates a quantile plot for cputime,
    saving it directly to a PDF file.

    Args:
        csv_path (str): The file path to the CSV/TSV results.
    """
    try:
        # Read the tab-separated file with a multi-level header.
        df = pd.read_csv(csv_path, header=[0, 1, 2], index_col=0, sep='\t')
    except FileNotFoundError:
        print(f"Error: The file '{csv_path}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    # Identify the unique tool configurations from the 'run set' header.
    run_sets = df.columns.get_level_values('run set').unique()

    # --- Plotting ---
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(12, 8))

    # Colors chosen to match the second image.
    colors = ['#d2b48c', '#8c564b', '#ff7f0e', '#17becf']
    
    print("Processing configurations...")
    # Loop through each configuration to plot its data.
    for i, run_set in enumerate(run_sets):
        run_set_df = df.xs(run_set, level='run set', axis=1)

        try:
            status_col = run_set_df.columns[run_set_df.columns.get_level_values(1) == 'status'][0]
            cputime_col = run_set_df.columns[run_set_df.columns.get_level_values(1) == 'cputime (s)'][0]
        except IndexError:
            print(f"Warning: Columns not found for '{run_set}'. Skipping.")
            continue
            
        # Filter for "Correct only" results.
        correct_mask = (run_set_df[status_col] == 'true') | \
                       (run_set_df[status_col].astype(str).str.startswith('false('))
        
        correct_times = run_set_df.loc[correct_mask, cputime_col]
        
        # Convert CPU times to numeric format and sort them.
        cputime_numeric = pd.to_numeric(correct_times, errors='coerce').dropna().sort_values()

        if cputime_numeric.empty:
            print(f"No correct results with valid cputime for: {run_set}")
            continue

        print(f"Plotting for: {run_set} ({len(cputime_numeric)} correct results)")

        # Prepare data for plotting.
        y_values = cputime_numeric.values
        x_values = np.arange(1, len(y_values) + 1)

        # Plot the quantile data for the current configuration.
        plt.plot(x_values, y_values, marker='o', linestyle='-', markersize=4, label=run_set, color=colors[i % len(colors)])

    # --- Final Plot Customization ---
    plt.yscale('log')
    plt.xlabel('Number of Solved Tasks', fontsize=12)
    plt.ylabel('CPU Time (s)', fontsize=12)
    plt.title('CPU Time Quantile Plot', fontsize=14)
    
    # Position the legend in the top-left corner.
    plt.legend(title='Configurations', loc='upper left')
    
    # Use a light, dotted grid style.
    plt.grid(True, which="both", ls=":", linewidth=0.6, color='lightgray')
    
    # Save the plot to a PDF file.
    # bbox_inches='tight' ensures that labels are not cut off.
    try:
        plt.savefig("cputime_quantile_plot.pdf", bbox_inches='tight')
        print("\nPlot successfully saved as 'cputime_quantile_plot.pdf'")
    except Exception as e:
        print(f"\nAn error occurred while saving the PDF: {e}")

# Run the function when the script is executed.
if __name__ == '__main__':
    generate_quantile_plot_pdf(CSV_FILE_PATH)

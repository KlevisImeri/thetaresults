import os
import pandas as pd

def analyze_heuristic_performance(csv_filepath, logs_dir):
    """
    Analyzes the performance of a timeout-prediction heuristic with detailed logging.
    This version defines an actual timeout based on the 'status' column and skips empty/incomplete logs.

    Args:
        csv_filepath (str): Path to the CSV file with benchmark results.
        logs_dir (str): Path to the directory containing the log files with predictions.
    """
    try:
        # Load the CSV with a multi-level header, using tab as a separator.
        df = pd.read_csv(csv_filepath, header=[1, 2], index_col=0, sep='\t')
        
        # Clean up column names to remove any extra whitespace.
        cleaned_columns = [tuple(str(s).strip() for s in col) for col in df.columns]
        df.columns = pd.MultiIndex.from_tuples(cleaned_columns)
        
    except FileNotFoundError:
        print(f"Error: The file '{csv_filepath}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        print("Please ensure the CSV is correctly formatted (tab-separated with 3 header rows).")
        return

    # Initialize counters
    true_positives, true_negatives, false_positives, false_negatives = 0, 0, 0, 0
    skipped_count = 0

    # The column representing the baseline (our ground truth)
    baseline_col_name = 'PredCart().SV-COMP25_unreach-call'

    # Iterate over each program run in the CSV
    for index, row in df.iterrows():
        program_name_full = row.name
        
        if not program_name_full or pd.isna(program_name_full):
            print("Skipping: Row has no program name (likely an empty row).")
            skipped_count += 1
            continue

        try:
            baseline_status = str(row[(baseline_col_name, 'status')]).strip()
        except KeyError:
            print(f"CRITICAL ERROR: The ground truth column '{baseline_col_name}' was not found in the CSV.")
            return

        is_timeout_actual = 'TIMEOUT' in baseline_status
        
        if 'ERROR' in baseline_status or 'OUT OF MEMORY' in baseline_status:
            # print(f"Skipping '{program_name_full}': Baseline status was '{baseline_status}'.")
            skipped_count += 1
            continue
        
        base_program_name = os.path.basename(program_name_full)
        log_filename = f"SV-COMP25_unreach-call.{base_program_name}.log"
        log_filepath = os.path.join(logs_dir, log_filename)
        predicted_timeout = False

        try:
            with open(log_filepath, 'r', encoding='utf-8', errors='ignore') as f:
                log_content = f.read()
                
                if "server:" not in log_content:
                    print(f"Skipping '{program_name_full}': Log file appears to be empty or incomplete.")
                    skipped_count += 1
                    continue

                if "java.util.UnknownFormatConversionException" in log_content:
                    print(f"Skipping '{program_name_full}': Log file contains a tool crash (UnknownFormatConversionException).")
                    skipped_count += 1
                    continue

                if "--------Iteration time heuristic predicts timeout--------" in log_content or \
                   "----Iteration time heuristic predicts state space explosion----" in log_content:
                    predicted_timeout = True

        except FileNotFoundError:
            print(f"Skipping '{program_name_full}': Log file not found at '{log_filepath}'.")
            skipped_count += 1
            continue

        # Classify the result
        if predicted_timeout and is_timeout_actual:
            true_positives += 1
        elif not predicted_timeout and not is_timeout_actual:
            true_negatives += 1
        elif predicted_timeout and not is_timeout_actual:
            false_positives += 1
        elif not predicted_timeout and is_timeout_actual:
            print(f"[FN]: {program_name_full}")
            false_negatives += 1

    # --- Calculate and Display Metrics ---
    total = true_positives + true_negatives + false_positives + false_negatives
    print(f"\n--- Analysis Complete ---")
    print(f"Total rows processed for metrics: {total}")
    print(f"Total rows skipped: {skipped_count}")
    
    if total == 0:
        print("\nNo valid data was processed. Please check the 'Skipping...' messages above for reasons.")
        return

    accuracy = (true_positives + true_negatives) / total if total > 0 else 0
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    specificity = true_negatives / (true_negatives + false_positives) if (true_negatives + false_positives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print("\n--- Heuristic Performance Metrics ---")
    print(f"True Positives (TP):  {true_positives}")
    print(f"True Negatives (TN):  {true_negatives}")
    print(f"False Positives (FP): {false_positives}")
    print(f"False Negatives (FN): {false_negatives}")
    print("-" * 35)
    print(f"Accuracy:    {accuracy:.4f}")
    print(f"Precision:   {precision:.4f}")
    print(f"Recall:      {recall:.4f}")
    print(f"Specificity: {specificity:.4f}")
    print(f"F1 Score:    {f1_score:.4f}")
    print("--------------------------------------")


if __name__ == "__main__":
    CSV_FILE_PATH = './results/4:PredCart(900, true, true) -> KInd() | 4:PredCart()/results.2025-11-02_13-31-48.table.csv'
    LOG_FILES_DIR = './results/baseline/4:PredCart(900, true, true) -> KInd()/PredCart(900, true, true) -> KInd().2025-10-08_08-29-11.logfiles'
    
    analyze_heuristic_performance(CSV_FILE_PATH, LOG_FILES_DIR)

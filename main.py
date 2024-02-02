from pathlib import Path
import cash_on_hand, profit_loss, overheads

overheads.find_highest_overhead(Path(r"csv_reports\Overheads.csv"))
cash_on_hand.analyze_cash_on_hand(Path(r"csv_reports\Cash_on_Hand.csv"))
profit_loss.analyze_netprofit(Path(r"csv_reports\Profits_and_Loss.csv"))

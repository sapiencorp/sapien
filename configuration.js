{
  "name": "SapienTradeBot",
  "task": "trade",
  "parameters": {
    "token_pair": " /SOL",
    "strategy": "simple_moving_average",
    "threshold": "0.01"
  }
}

{
  "name": "WalletGuardian",
  "task": "wallet_management",
  "parameters": {
    "wallet_address": "So1m2L27uJ3e6nZJ2i6yqJ86zV",
    "threshold_for_alert": "1000"
  }
}

{
  "name": "AssetTracker",
  "task": "asset_tracking",
  "parameters": {
    "tokens_to_track": "SOL,RAY,SRM",
    "interval": "1h"
  }
}

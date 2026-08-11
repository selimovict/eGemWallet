import json
from datetime import datetime, timezone

import pymssql

from dal.database import Database
from models.save_round_service_model import SaveRoundResponse


def _json_or_null(value):
    """Serijalizira value u JSON string; vraca None za None, prazan dict ili praznu listu."""
    if value is None:
        return None
    if isinstance(value, (dict, list)) and not value:
        return None
    return json.dumps(value, ensure_ascii=False)


class SaveRoundBLL:

    @staticmethod
    def save(body: dict) -> SaveRoundResponse:
        feature       = body.get("feature") or {}
        purchase_type = body.get("purchase_type", "")

        is_feature_buy     = purchase_type == "free_spins"
        is_scatter_trigger = bool(feature.get("triggered", False))
        free_spin          = is_feature_buy or is_scatter_trigger

        if is_feature_buy:
            free_spin_source = "purchase"
        elif is_scatter_trigger:
            free_spin_source = "scatter_trigger"
        else:
            free_spin_source = None

        balance_after  = float(body.get("balance", 0))
        total_bet      = float(body.get("total_bet", 0))
        total_win      = float(body.get("total_win", 0))
        balance_before = round(balance_after + total_bet - total_win, 4)

        external_id      = body.get("external_round_identifier") or None
        has_external_id  = external_id is not None
        now              = datetime.now(timezone.utc).replace(tzinfo=None)
        game_id          = body.get("game_id", "")

        ext_col = "ExternalRoundIdentifier," if has_external_id else ""
        ext_val = "%(ExternalRoundIdentifier)s," if has_external_id else ""

        sql = f"""
            INSERT INTO dbo.GamePlayRound (
                {ext_col}
                ParentRoundID,
                MachineID,
                MachineName,
                FreeSpin,
                FreeSpinSource,
                UserID,
                Lines,
                AmountInPerLine,
                TotalAmountIn,
                AmountOut,
                BaseWin,
                ScatterWin,
                FreeSpinsWin,
                BalanceBefore,
                BalanceAfter,
                Currency,
                Success,
                Message,
                DateTimeStarted,
                DateTimeDone,
                UserJSON,
                BalanceJSON,
                GameJSON,
                ReelsJSON,
                FeatureJSON,
                FeatureBuyJSON,
                DetailsJSON
            )
            OUTPUT INSERTED.RoundID, INSERTED.ExternalRoundIdentifier
            VALUES (
                {ext_val}
                NULL,
                %(MachineID)s,
                %(MachineName)s,
                %(FreeSpin)s,
                %(FreeSpinSource)s,
                %(UserID)s,
                %(Lines)s,
                %(AmountInPerLine)s,
                %(TotalAmountIn)s,
                %(AmountOut)s,
                %(BaseWin)s,
                %(ScatterWin)s,
                %(FreeSpinsWin)s,
                %(BalanceBefore)s,
                %(BalanceAfter)s,
                %(Currency)s,
                %(Success)s,
                %(Message)s,
                %(DateTimeStarted)s,
                %(DateTimeDone)s,
                NULL,
                NULL,
                %(GameJSON)s,
                %(ReelsJSON)s,
                %(FeatureJSON)s,
                %(FeatureBuyJSON)s,
                %(DetailsJSON)s
            )
        """

        params = {
            "MachineID":               game_id,
            "MachineName":             game_id,
            "FreeSpin":                1 if free_spin else 0,
            "FreeSpinSource":          free_spin_source,
            "UserID":                  body.get("player_id", ""),
            "Lines":                   int(body.get("lines", 0)),
            "AmountInPerLine":         float(body.get("bet_per_line", 0)),
            "TotalAmountIn":           total_bet,
            "AmountOut":               total_win,
            "BaseWin":                 float(body.get("base_win", 0)),
            "ScatterWin":              float(body.get("scatter_win", 0)),
            "FreeSpinsWin":            float(body.get("free_spins_win", 0)),
            "BalanceBefore":           balance_before,
            "BalanceAfter":            balance_after,
            "Currency":                body.get("currency", ""),
            "Success":                 1 if body.get("success", True) else 0,
            "Message":                 body.get("message", ""),
            "DateTimeStarted":         now,
            "DateTimeDone":            now,
            "GameJSON":                json.dumps(body, ensure_ascii=False),
            "ReelsJSON":               _json_or_null(body.get("reels")),
            "FeatureJSON":             _json_or_null(body.get("feature")),
            "FeatureBuyJSON":          _json_or_null(body.get("feature_buy")),
            "DetailsJSON":             _json_or_null(body.get("details")),
        }

        if has_external_id:
            params["ExternalRoundIdentifier"] = external_id

        try:
            row = Database.query_single(sql, params)
        except pymssql.IntegrityError as e:
            err_num = e.args[0] if e.args else 0
            if err_num in (2601, 2627) and has_external_id:
                existing = Database.query_single(
                    "SELECT RoundID, ExternalRoundIdentifier FROM dbo.GamePlayRound"
                    " WHERE ExternalRoundIdentifier = %(ext_id)s",
                    {"ext_id": external_id},
                )
                resp = SaveRoundResponse()
                resp.RoundID                 = existing["RoundID"] if existing else None
                resp.ExternalRoundIdentifier = external_id
                resp.Success                 = True
                resp.Message                 = "Round already saved."
                return resp
            raise

        resp = SaveRoundResponse()
        resp.RoundID                  = row["RoundID"] if row else None
        resp.ExternalRoundIdentifier  = row["ExternalRoundIdentifier"] if row else None
        resp.Success                  = row is not None
        resp.Message                  = "Round saved." if row else "Insert failed."
        return resp

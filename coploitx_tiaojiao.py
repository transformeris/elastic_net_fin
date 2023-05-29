import akshare as ak
import pandas as pd
import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from akshare.stock_feature.stock_three_report_em import _stock_balance_sheet_by_report_ctype_em
from functools import lru_cache
trans={
    "SECUCODE": "证券代码",
    "SECURITY_CODE": "证券内部编码",
    "SECURITY_NAME_ABBR": "证券简称",
    "ORG_CODE": "机构编码",
    "ORG_TYPE": "机构类型",
    "REPORT_DATE": "报告日期",
    "REPORT_TYPE": "报告类型",
    "REPORT_DATE_NAME": "报告期名称",
    "SECURITY_TYPE_CODE": "证券类型编码",
    "NOTICE_DATE": "公告日期",
    "UPDATE_DATE": "更新日期",
    "CURRENCY": "货币资金",
    "ACCEPT_DEPOSIT_INTERBANK": "同业存放",
    "ACCOUNTS_PAYABLE": "应付账款",
    "ACCOUNTS_RECE": "应收账款",
    "ACCRUED_EXPENSE": "预提费用",
    "ADVANCE_RECEIVABLES": "预收款项",
    "AGENT_TRADE_SECURITY": "代理买卖证券款",
    "AGENT_UNDERWRITE_SECURITY": "代理承销证券款",
    "AMORTIZE_COST_FINASSET": "摊销费用-金融资产",
    "AMORTIZE_COST_FINLIAB": "摊销费用-金融负债",
    "AMORTIZE_COST_NCFINASSET": "摊销费用-非金融资产",
    "AMORTIZE_COST_NCFINLIAB": "摊销费用-非金融负债",
    "APPOINT_FVTPL_FINASSET": "指定为以公允价值计量且其变动计入当期损益的金融资产",
    "APPOINT_FVTPL_FINLIAB": "指定为以公允价值计量且其变动计入当期损益的金融负债",
    "ASSET_BALANCE": "资产总额",
    "ASSET_OTHER": "其他资产",
    "ASSIGN_CASH_DIVIDEND": "分配股利、利润或偿付利息所支付的现金",
    "AVAILABLE_SALE_FINASSET": "可供出售金融资产",
    "BOND_PAYABLE": "应付债券",
    "BORROW_FUND": "拆入资金",
    "BUY_RESALE_FINASSET": "买入返售金融资产",
    "CAPITAL_RESERVE": "资本公积",
    "CIP": "在建工程",
    "CONSUMPTIVE_BIOLOGICAL_ASSET": "消耗性生物资产",
    "CONTRACT_ASSET": "合同资产",
    "CONTRACT_LIAB": "合同负债",
    "CONVERT_DIFF": "外币报表折算差额",
    "CREDITOR_INVEST": "应付投资款",
    "CURRENT_ASSET_BALANCE": "流动资产合计",
    "CURRENT_ASSET_OTHER": "流动资产其他项目",
    "CURRENT_LIAB_BALANCE": "流动负债合计",
    "CURRENT_LIAB_OTHER": "流动负债其他项目",
    "DEFER_INCOME": "递延收益",
    "DEFER_INCOME_1YEAR": "一年内递延收益",
    "DEFER_TAX_ASSET": "递延所得税资产",
    "DEFER_TAX_LIAB": "递延所得税负债",
    "DERIVE_FINASSET": "衍生金融资产",
    "DERIVE_FINLIAB": "衍生金融负债",
    "DEVELOP_EXPENSE": "开发支出",
    "DIV_HOLDSALE_ASSET": "持有待售的资产",
    "DIV_HOLDSALE_LIAB": "持有待售的负债",
    "DIVIDEND_PAYABLE": "应付股利",
    "DIVIDEND_RECE": "应收股利",
    "EQUITY_BALANCE": "所有者权益合计",
    "EQUITY_OTHER": "所有者权益其他项目",
    "EXPORT_REFUND_RECE": "出口退税",
    "FEE_COMMISSION_PAYABLE": "应付手续费及佣金",
    "FIN_FUND": "融资租赁负债",
    "FINANCE_RECE": "融资租赁资产",
    "FIXED_ASSET": "固定资产",
    "FIXED_ASSET_DISPOSAL": "固定资产清理",
    "FVTOCI_FINASSET": "以后按公允价值计量且其变动计入其他综合收益的金融资产",
    "FVTOCI_NCFINASSET": "以后按公允价值计量且其变动计入其他综合收益的非金融资产",
    "FVTPL_FINASSET": "以公允价值计量且其变动计入当期损益的金融资产",
    "FVTPL_FINLIAB": "以公允价值计量且其变动计入当期损益的金融负债",
    "GENERAL_RISK_RESERVE": "一般风险准备",
    "GOODWILL": "商誉",
    "HOLD_MATURITY_INVEST": "持有至到期投资",
    "HOLDSALE_ASSET": "持有待售的资产",
    "HOLDSALE_LIAB": "持有待售的负债",
    "INSURANCE_CONTRACT_RESERVE": "保险合同准备金",
    "INTANGIBLE_ASSET": "无形资产",
    "INTEREST_PAYABLE": "应付利息",
    "INTEREST_RECE": "应收利息",
    "INTERNAL_PAYABLE": "内部应付款",
    "INTERNAL_RECE": "内部应收款",
    "INVENTORY": "存货",
    "INVEST_REALESTATE": "投资性房地产",
    "LEASE_LIAB": "租赁负债",
    "LEND_FUND": "拆出资金",
    "LIAB_BALANCE": "负债合计",
    "LIAB_EQUITY_BALANCE": "负债和所有者权益合计",
    "LIAB_EQUITY_OTHER": "负债和所有者权益其他项目",
    "LIAB_OTHER": "负债其他项目",
    "LOAN_ADVANCE": "发放贷款及垫款",
    "LOAN_PBC": "拆出资金",
    "LONG_EQUITY_INVEST": "长期股权投资",
    "LONG_LOAN": "长期借款",
    "LONG_PAYABLE": "长期应付款",
    "LONG_PREPAID_EXPENSE": "长期待摊费用",
    "LONG_RECE": "长期应收款",
    "LONG_STAFFSALARY_PAYABLE": "长期应付职工薪酬",
    "MINORITY_EQUITY": "少数股东权益",
    "MONETARYFUNDS": "货币资金",
    "NONCURRENT_ASSET_1YEAR": "一年内到期的非流动资产",
    "NONCURRENT_ASSET_BALANCE": "非流动资产合计",
    "NONCURRENT_ASSET_OTHER": "非流动资产其他项目",
    "NONCURRENT_LIAB_1YEAR": "一年内到期的非流动负债",
    "NONCURRENT_LIAB_BALANCE": "非流动负债合计",
    "NONCURRENT_LIAB_OTHER": "非流动负债其他项目",
    "NOTE_ACCOUNTS_PAYABLE": "应付账款",
    "NOTE_ACCOUNTS_RECE": "应收账款",
    "NOTE_PAYABLE": "应付票据",
    "NOTE_RECE": "应收票据",
    "OIL_GAS_ASSET": "油气资产",
    "OTHER_COMPRE_INCOME": "其他综合收益",
    "OTHER_CREDITOR_INVEST": "其他债权投资",
    "OTHER_CURRENT_ASSET": "其他流动资产",
    "OTHER_CURRENT_LIAB": "其他流动负债",
    "OTHER_EQUITY_INVEST": "其他权益工具投资",
    "OTHER_EQUITY_OTHER": "其他权益工具",
    "OTHER_EQUITY_TOOL": "其他权益工具",
    "OTHER_NONCURRENT_ASSET": "其他非流动资产",
    "OTHER_NONCURRENT_FINASSET": "其他非流动金融资产",
    "OTHER_NONCURRENT_LIAB": "其他非流动负债",
    "OTHER_PAYABLE": "其他应付款",
    "OTHER_RECE": "其他应收款",
    "PARENT_EQUITY_BALANCE": "归属于母公司股东权益",
    "PARENT_EQUITY_OTHER": "归属于母公司的其他权益工具",
    "PERPETUAL_BOND": "永续债",
    "PERPETUAL_BOND_PAYBALE": "应付永续债",
    "PREDICT_CURRENT_LIAB": "预计流动负债",
    "PREDICT_LIAB": "预计负债",
    "PREFERRED_SHARES": "优先股",
    "PREFERRED_SHARES_PAYBALE": "应付优先股",
    "PREMIUM_RECE": "预收保费",
    "PREPAYMENT": "预付款项",
    "PRODUCTIVE_BIOLOGY_ASSET": "生产性生物资产",
    "PROJECT_MATERIAL": "工程物资",
    "RC_RESERVE_RECE": "应收保费返还款",
    "REINSURE_PAYABLE": "应付分保账款",
    "REINSURE_RECE": "应收分保账款",
    "SELL_REPO_FINASSET": "卖出回购金融资产款",
    "SETTLE_EXCESS_RESERVE": "结算备付金",
    "SHARE_CAPITAL": "股本",
    "SHORT_BOND_PAYABLE": "应付短期债券",
    "SHORT_FIN_PAYABLE": "应付短期融资款",
    "SHORT_LOAN": "短期借款",
    "SPECIAL_PAYABLE": "专项应付款",
    "SPECIAL_RESERVE": "专项储备",
    "STAFF_SALARY_PAYABLE": "应付职工薪酬",
    "SUBSIDY_RECE": "应收补贴款",
    "SURPLUS_RESERVE": "盈余公积",
    "TAX_PAYABLE": "应交税费",
    "TOTAL_ASSETS": "资产总计",
    "TOTAL_CURRENT_ASSETS": "流动资产合计",
    "TOTAL_CURRENT_LIAB": "流动负债合计",
    "TOTAL_EQUITY": "所有者权益合计",
    "TOTAL_LIAB_EQUITY": "负债和所有者权益总计",
    "TOTAL_LIABILITIES": "负债合计",
    "TOTAL_NONCURRENT_ASSETS": "非流动资产合计",
    "TOTAL_NONCURRENT_LIAB": "非流动负债合计",
    "TOTAL_OTHER_PAYABLE": "其他应付款合计",
    "TOTAL_OTHER_RECE": "其他应收款合计",
    "TOTAL_PARENT_EQUITY": "归属于母公司股东权益合计",
    "TRADE_FINASSET": "交易性金融资产",
    "TRADE_FINASSET_NOTFVTPL": "交易性金融资产（不公允价值变动计入当期损益）",
    "TRADE_FINLIAB": "交易性金融负债",
    "TRADE_FINLIAB_NOTFVTPL": "交易性金融负债（不公允价值变动计入当期损益）",
    "TREASURY_SHARES": "库存股",
    "UNASSIGN_RPOFIT": "未分配利润",
    "UNCONFIRM_INVEST_LOSS": "未确认投资损失",
    "USERIGHT_ASSET": "使用权资产",
    "ACCEPT_DEPOSIT_INTERBANK_YOY": "同业存放款项",
    "ACCOUNTS_PAYABLE_YOY": "应付账款",
    "ACCOUNTS_RECE_YOY": "应收账款",
    "ACCRUED_EXPENSE_YOY": "预提费用",
    "ADVANCE_RECEIVABLES_YOY": "预收款项",
    "AGENT_TRADE_SECURITY_YOY": "代理买卖证券款",
    "AGENT_UNDERWRITE_SECURITY_YOY": "代理承销证券款",
    "AMORTIZE_COST_FINASSET_YOY": "摊销交易性金融资产损失",
    "AMORTIZE_COST_FINLIAB_YOY": "摊销交易性金融负债费用",
    "AMORTIZE_COST_NCFINASSET_YOY": "摊销非交易性金融资产损失",
    "AMORTIZE_COST_NCFINLIAB_YOY": "摊销非交易性金融负债费用",
    "APPOINT_FVTPL_FINASSET_YOY": "应收款项类投资",
    "APPOINT_FVTPL_FINLIAB_YOY": "应付款项类投资",
    "ASSET_BALANCE_YOY": "资产总额",
    "ASSET_OTHER_YOY": "其他资产",
    "ASSIGN_CASH_DIVIDEND_YOY": "分配股利、利润或偿付利息所支付的现金",
    "AVAILABLE_SALE_FINASSET_YOY": "可供出售金融资产",
    "BOND_PAYABLE_YOY": "应付债券",
    "BORROW_FUND_YOY": "借款",
    "BUY_RESALE_FINASSET_YOY": "买入返售金融资产款",
    "CAPITAL_RESERVE_YOY": "资本公积",
    "CIP_YOY": "在建工程",
    "CONSUMPTIVE_BIOLOGICAL_ASSET_YOY": "消耗性生物资产",
    "CONTRACT_ASSET_YOY": "合同资产",
    "CONTRACT_LIAB_YOY": "合同负债",
    "CONVERT_DIFF_YOY": "外币报表折算差额",
    "CREDITOR_INVEST_YOY": "债权投资",
    "CURRENT_ASSET_BALANCE_YOY": "流动资产合计",
    "CURRENT_ASSET_OTHER_YOY": "其他流动资产",
    "CURRENT_LIAB_BALANCE_YOY": "流动负债合计",
    "CURRENT_LIAB_OTHER_YOY": "其他流动负债",
    "DEFER_INCOME_1YEAR_YOY": "一年内的递延收益",
    "DEFER_INCOME_YOY": "递延收益",
    "DEFER_TAX_ASSET_YOY": "递延所得税资产",
    "DEFER_TAX_LIAB_YOY": "递延所得税负债",
    "DERIVE_FINASSET_YOY": "衍生金融资产",
    "DERIVE_FINLIAB_YOY": "衍生金融负债",
    "DEVELOP_EXPENSE_YOY": "研发费用同比增长率",
    "DIV_HOLDSALE_ASSET_YOY": "持有待售资产减值准备同比增长率",
    "DIV_HOLDSALE_LIAB_YOY": "持有待售负债减值准备同比增长率",
    "DIVIDEND_PAYABLE_YOY": "应付股利同比增长率",
    "DIVIDEND_RECE_YOY": "应收股利同比增长率",
    "EQUITY_BALANCE_YOY": "股东权益同比增长率",
    "EQUITY_OTHER_YOY": "其他股东权益同比增长率",
    "EXPORT_REFUND_RECE_YOY": "出口退税同比增长率",
    "FEE_COMMISSION_PAYABLE_YOY": "应付手续费及佣金同比增长率",
    "FIN_FUND_YOY": "融资租赁资产同比增长率",
    "FINANCE_RECE_YOY": "融资租赁负债同比增长率",
    "FIXED_ASSET_DISPOSAL_YOY": "固定资产处置收益同比增长率",
    "FIXED_ASSET_YOY": "固定资产同比增长率",
    "FVTOCI_FINASSET_YOY": "以公允价值计量且其变动计入其他综合收益的金融资产同比增长率",
    "FVTOCI_NCFINASSET_YOY": "以公允价值计量且其变动计入其他综合收益的非流动金融资产同比增长率",
    "FVTPL_FINASSET_YOY": "以公允价值计量且其变动计入当期损益的金融资产同比增长率",
    "FVTPL_FINLIAB_YOY": "以公允价值计量且其变动计入当期损益的金融负债同比增长率",
    "GENERAL_RISK_RESERVE_YOY": "一般风险准备同比增长率",
    "GOODWILL_YOY": "商誉同比增长率",
    "HOLD_MATURITY_INVEST_YOY": "持有至到期投资同比增长率",
    "HOLDSALE_ASSET_YOY": "持有待售资产同比增长率",
    "HOLDSALE_LIAB_YOY": "持有待售负债同比增长率",
    "INSURANCE_CONTRACT_RESERVE_YOY": "保险合同准备金同比增长率",
    "INTANGIBLE_ASSET_YOY": "无形资产同比增长率",
    "INTEREST_PAYABLE_YOY": "应付利息同比增长率",
    "INTEREST_RECE_YOY": "应收利息同比增长率",
    "INTERNAL_PAYABLE_YOY": "内部应付款同比增长率",
    "INTERNAL_RECE_YOY": "内部应收款同比增长率",
    "INVENTORY_YOY": "存货同比增长率",
    "INVEST_REALESTATE_YOY": "投资性房地产同比增长率",
    "LEASE_LIAB_YOY": "租赁负债同比增长率",
    "LEND_FUND_YOY": "拆出资金同比增长率",
    "LIAB_BALANCE_YOY": "负债总额同比增长率",
    "LIAB_EQUITY_BALANCE_YOY": "负债和股东权益总额同比增长率",
    "LIAB_EQUITY_OTHER_YOY": "其他负债和股东权益同比增长率",
    "LIAB_OTHER_YOY": "其他负债同比增长率",
    "LOAN_ADVANCE_YOY": "发放贷款及垫款同比增长率",
    "LOAN_PBC_YOY": "拆入资金同比增长率",
    "LONG_EQUITY_INVEST_YOY": "长期股权投资同比增长率",
    "LONG_LOAN_YOY": "长期借款同比增长率",
    "LONG_PAYABLE_YOY": "长期应付款同比增长率",
    "LONG_PREPAID_EXPENSE_YOY": "长期待摊费用同比增长率",
    "LONG_RECE_YOY": "长期应收款同比增长率",
    "LONG_STAFFSALARY_PAYABLE_YOY": "长期员工薪酬应付款同比增长率",
    "MINORITY_EQUITY_YOY": "少数股东权益同比增长率",
    "MONETARYFUNDS_YOY": "货币资金同比增长率",
    "NONCURRENT_ASSET_1YEAR_YOY": "一年内到期的非流动资产同比增长率",
    "NONCURRENT_ASSET_BALANCE_YOY": "非流动资产总额同比增长率",
    "NONCURRENT_ASSET_OTHER_YOY": "其他非流动资产同比增长率",
    "NONCURRENT_LIAB_1YEAR_YOY": "一年内到期的非流动负债同比增长率",
    "NONCURRENT_LIAB_BALANCE_YOY": "非流动负债总额同比增长率",
    "NONCURRENT_LIAB_OTHER_YOY": "其他非流动负债同比增长率",
    "NOTE_ACCOUNTS_PAYABLE_YOY": "应付票据同比增长率",
    "NOTE_ACCOUNTS_RECE_YOY": "应收票据同比增长率",
    "NOTE_PAYABLE_YOY": "应付账款同比增长率",
    "NOTE_RECE_YOY": "应收账款同比增长率",
    "OIL_GAS_ASSET_YOY": "油气资产同比增长率",
    "OTHER_COMPRE_INCOME_YOY": "其他综合收益同比增长率",
    "OTHER_CREDITOR_INVEST_YOY": "其他债权投资同比增长率",
    "OTHER_CURRENT_ASSET_YOY": "其他流动资产同比增长率",
    "OTHER_CURRENT_LIAB_YOY": "其他流动负债同比增长率",
    "OTHER_EQUITY_INVEST_YOY": "其他权益工具投资同比增长率",
    "OTHER_EQUITY_OTHER_YOY": "其他权益工具及其他股东权益同比增长率",
    "OTHER_EQUITY_TOOL_YOY": "其他权益工具同比增长率",
    "OTHER_NONCURRENT_ASSET_YOY": "其他非流动资产同比增长率",
    "OTHER_NONCURRENT_FINASSET_YOY": "其他非流动金融资产同比增长率",
    "OTHER_NONCURRENT_LIAB_YOY": "其他非流动负债同比增长率",
    "OTHER_PAYABLE_YOY": "其他应付款同比增长率",
    "OTHER_RECE_YOY": "其他应收款同比增长率",
    "PARENT_EQUITY_BALANCE_YOY": "归属于母公司股东权益同比增长率",
    "PARENT_EQUITY_OTHER_YOY": "归属于母公司其他权益工具及其他股东权益同比增长率",
    "PERPETUAL_BOND_PAYBALE_YOY": "永续债应付款同比增长率",
    "PERPETUAL_BOND_YOY": "永续债同比增长率",
    "PREDICT_CURRENT_LIAB_YOY": "预计流动负债同比增长率",
    "PREDICT_LIAB_YOY": "预计负债同比增长率",
    "PREFERRED_SHARES_PAYBALE_YOY": "应付优先股同比增长率",
    "PREFERRED_SHARES_YOY": "优先股同比增长率",
    "PREMIUM_RECE_YOY": "预收保费同比增长率",
    "PREPAYMENT_YOY": "预付款项同比增长率",
    "PRODUCTIVE_BIOLOGY_ASSET_YOY": "生产性生物资产同比增长率",
    "PROJECT_MATERIAL_YOY": "工程物资同比增长率",
    "RC_RESERVE_RECE_YOY": "应收款项类投资收益同比增长率",
    "REINSURE_PAYABLE_YOY": "应付分保账款同比增长率",
    "REINSURE_RECE_YOY": "应收分保账款同比增长率",
    "SELL_REPO_FINASSET_YOY": "卖出回购金融资产同比增长率",
    "SETTLE_EXCESS_RESERVE_YOY": "结算备付金同比增长率",
    "SHARE_CAPITAL_YOY": "股本同比增长率",
    "SHORT_BOND_PAYABLE_YOY": "应付短期债券同比增长率",
    "SHORT_FIN_PAYABLE_YOY": "应付短期融资款同比增长率",
    "SHORT_LOAN_YOY": "短期借款同比增长率",
    "SPECIAL_PAYABLE_YOY": "专项应付款同比增长率",
    "SPECIAL_RESERVE_YOY": "专项储备同比增长率",
    "STAFF_SALARY_PAYABLE_YOY": "应付职工薪酬同比增长率",
    "SUBSIDY_RECE_YOY": "应收补贴款同比增长率",
    "SURPLUS_RESERVE_YOY": "盈余公积同比增长率",
    "TAX_PAYABLE_YOY": "应交税费同比增长率",
    "TOTAL_ASSETS_YOY": "资产总额同比增长率",
    "TOTAL_CURRENT_ASSETS_YOY": "流动资产合计同比增长率",
    "TOTAL_CURRENT_LIAB_YOY": "流动负债合计同比增长率",
    "TOTAL_EQUITY_YOY": "所有者权益合计同比增长率",
    "TOTAL_LIAB_EQUITY_BALANCE_YOY": "负债和所有者权益总额同比增长率",
    "TOTAL_LIABILITIES_YOY": "负债合计同比增长率",
    "TOTAL_NONCURRENT_ASSETS_YOY": "非流动资产合计同比增长率",
    "TOTAL_NONCURRENT_LIAB_YOY": "非流动负债合计同比增长率",
    "TOTAL_OTHER_PAYABLE_YOY": "其他应付款合计同比增长率",
    "TOTAL_OTHER_RECE_YOY": "其他应收款合计同比增长率",
    "TOTAL_PARENT_EQUITY_YOY": "归属于母公司所有者权益同比增长率",
    "TRADE_FINASSET_NOTFVTPL_YOY": "交易性金融资产（不公允价值计量且其变动计入当期损益）同比增长率",
    "TRADE_FINASSET_YOY": "交易性金融资产同比增长率",
    "TRADE_FINLIAB_NOTFVTPL_YOY": "交易性金融负债（不公允价值计量且其变动计入当期损益）同比增长率",
    "TRADE_FINLIAB_YOY": "交易性金融负债同比增长率",
    "TREASURY_SHARES_YOY": "减：库存股同比增长率",
    "UNASSIGN_RPOFIT_YOY": "未分配利润同比增长率",
    "UNCONFIRM_INVEST_LOSS_YOY": "未确认的投资损失同比增长率",
    "USERIGHT_ASSET_YOY": "使用权资产同比增长率",
    "OPINION_TYPE": "审计意见类型",
    "OSOPINION_TYPE": "其他审计结果类型",
    "LISTING_STATE": "上市状态",
    "timestamp": "时间戳"
}


def stock_balance_sheet_by_report_em(symbol: str = "SH600519") -> pd.DataFrame:
    """
    东方财富-股票-财务分析-资产负债表-按报告期
    https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=sh600519#lrb-0
    :param symbol: 股票代码; 带市场标识
    :type symbol: str
    :return: 资产负债表-按报告期
    :rtype: pandas.DataFrame
    """
    company_type = _stock_balance_sheet_by_report_ctype_em(symbol=symbol)
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/zcfzbDateAjaxNew"
    params = {
        "companyType": company_type,
        "reportDateType": "0",
        "code": symbol,
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"])
    temp_df["REPORT_DATE"] = pd.to_datetime(temp_df["REPORT_DATE"]).dt.date
    temp_df["REPORT_DATE"] = temp_df["REPORT_DATE"].astype(str)
    need_date = temp_df["REPORT_DATE"].tolist()
    sep_list = [
        ",".join(need_date[i : i + 5]) for i in range(0, len(need_date), 5)
    ]
    big_df = pd.DataFrame()
    for item in tqdm(sep_list, leave=False):
        url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/zcfzbAjaxNew"
        params = {
            "companyType": company_type,
            "reportDateType": "0",
            "reportType": "1",
            "dates": item,
            "code": symbol,
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    return big_df


# # stock_financial_report_sina_df = ak.stock_financial_report_sina(stock="sh600600", symbol="资产负债表")
# # print(stock_financial_report_sina_df)
# # biaotou=list(stock_financial_report_sina_df.columns)
# stock_balance_sheet_by_report_em_df = ak.stock_balance_sheet_by_report_em(symbol="SH600600")
# print(stock_balance_sheet_by_report_em_df)
#
# stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="600600", period="daily", start_date="20170301", end_date='20230907', adjust="")
#
#
# # 将时间戳列转换为 datetime 类型
# stock_balance_sheet_by_report_em_df['timestamp'] = pd.to_datetime(stock_balance_sheet_by_report_em_df['UPDATE_DATE'])
# stock_zh_a_hist_df['timestamp'] = pd.to_datetime(stock_zh_a_hist_df['日期'])
# stock_balance_sheet_by_report_em_df = stock_balance_sheet_by_report_em_df.sort_values('timestamp')
# # 使用 merge_asof() 函数按照时间戳合并两个 DataFrame
# merged_df = pd.merge_asof(stock_zh_a_hist_df, stock_balance_sheet_by_report_em_df, on='timestamp')
#
# # 输出合并后的 DataFrame
# print(merged_df)

# 获取 A 股股票列表
# stock_info_df = ak.stock_zh_a_spot()
# print(stock_info_df)

import akshare as ak
import pandas as pd

def merge_financial_report(stock_code, start_date, end_date):
    # 获取财务报表数据
    stock_financial_report_sina_df = ak.stock_financial_report_sina(stock=stock_code, symbol="资产负债表")
    # 获取行情数据
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=str(stock_code)[2:], period="daily", start_date=start_date, end_date=end_date, adjust="")
    # 将时间戳列转换为 datetime 类型
    stock_financial_report_sina_df['timestamp'] = pd.to_datetime(stock_financial_report_sina_df['更新日期'])
    stock_zh_a_hist_df['timestamp'] = pd.to_datetime(stock_zh_a_hist_df['日期'])
    # 对财务报表数据按照时间戳列进行排序
    stock_financial_report_sina_df = stock_financial_report_sina_df.sort_values('timestamp')
    # 使用 merge_asof() 函数按照时间戳合并两个 DataFrame
    merged_df = pd.merge_asof(stock_zh_a_hist_df, stock_financial_report_sina_df, on='timestamp')
    return merged_df

if __name__=='__main__':
    # aa=merge_financial_report('sz000001', "20150301", "20230301")
    import json

    # stock_balance_sheet_by_report_em_df = stock_balance_sheet_by_report_em_df.rename(columns=trans)
    zz=stock_balance_sheet_by_report_em("SH600600")
    zz=zz.rename(columns=trans)
    zz.to_csv('青岛啤酒.csv', encoding='utf-8-sig')
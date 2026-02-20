# screener/universe.py

LQ45_TICKERS = [
    "AALI.JK", "ACES.JK", "ADRO.JK", "AKRA.JK", "AMRT.JK",
    "ANTM.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK",
    "BBTN.JK", "BJTM.JK", "BMRI.JK", "BRPT.JK", "BUKA.JK",
    "CPIN.JK", "EMTK.JK", "ERAA.JK", "EXCL.JK", "GGRM.JK",
    "GOTO.JK", "HMSP.JK", "HRUM.JK", "ICBP.JK", "INCO.JK",
    "INDF.JK", "INKP.JK", "INTP.JK", "ITMG.JK", "JPFA.JK",
    "KLBF.JK", "MAPI.JK", "MBMA.JK", "MDKA.JK", "MEDC.JK",
    "MIKA.JK", "PGAS.JK", "PTBA.JK", "PTPP.JK", "SMGR.JK",
    "TBIG.JK", "TLKM.JK", "TOWR.JK", "UNTR.JK", "UNVR.JK",
]

def get_universe():
    return LQ45_TICKERS
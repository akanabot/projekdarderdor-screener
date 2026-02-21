# screener/universe.py

def get_universe():
    # Daftar emiten pilihan berdasarkan kategori
    watchlist = [
        # 1) Big Caps – Banking & Finance
        "BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK", "BRIS.JK", "ARTO.JK",
        "BNGA.JK", "NISP.JK", "PNBN.JK", "BBYB.JK", "BEST.JK", "FASW.JK",

        # 2) Telecom & Tech
        "TLKM.JK", "ISAT.JK", "EXCL.JK", "MTEL.JK", "GOTO.JK", "BUKA.JK", 
        "ACES.JK", "DCII.JK",

        # 3) Consumer & Retail
        "ICBP.JK", "INDF.JK", "MYOR.JK", "UNVR.JK", "HMSP.JK", "GGRM.JK", 
        "KLBF.JK", "CPIN.JK", "JPFA.JK", "SIDO.JK", "ULTJ.JK", "AMRT.JK", 
        "ERAA.JK", "LPPF.JK",

        # 4) Energy & Mining
        "ADRO.JK", "PTBA.JK", "ITMG.JK", "INDY.JK", "HRUM.JK", "TOBA.JK", 
        "MEDC.JK", "PGAS.JK", "AMMN.JK", "BRPT.JK", "TINS.JK", "ELSA.JK", 
        "ANTM.JK", "INCO.JK",

        # 5) Infrastructure, Property & Construction
        "ASII.JK", "WIKA.JK", "PTPP.JK", "ADHI.JK", "WSKT.JK", "WEGE.JK",
        "BSDE.JK", "CTRA.JK", "SMRA.JK", "PWON.JK", "ASRI.JK", "DMAS.JK",

        # 6) Industrial & Basic Materials
        "SMGR.JK", "INKP.JK", "TKIM.JK", "AKRA.JK", "MPPA.JK", "TOTO.JK", "TPMA.JK",

        # 7) Media & Advertising
        "SCMA.JK", "MNCN.JK", "ELTY.JK", "MARI.JK",

        # 8) Misc / Mid Cap High Liquidity
        "BMTR.JK", "CITY.JK", "BTON.JK", "FREN.JK", "LSIP.JK", "DILD.JK", "KPIG.JK"
    ]

    # Menghapus duplikat (jika ada) dan mengurutkan secara alfabetis
    unique_tickers = sorted(list(set(watchlist)))
    
    return unique_tickers
DIVIDENDS_URL = "https://bastter.com/mercado/webservices/WS_EmpresaNew.asmx/ListarCalendarioEmpresa"
SPLITS_URL = "https://bastter.com/mercado/webservices/WS_EmpresaNew.asmx/ListarEventoEmpresa"
PROVENTOS_FII_URL = "https://bastter.com/mercado/webservices/WS_FII.asmx/ProventoListar"
EVENTOS_FII_URL= "https://bastter.com/mercado/webservices/WS_FII.asmx/ListarEvento"
def get_header(name):
    return {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "en-US,en;q=0.9",
                "authority": "bastter.com",
                "content-type": "application/json; charset=UTF-8",
                "origin": "https://bastter.com",
                "referer": "https://bastter.com/mercado/fii/" + name,
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                "x-requested-with": "XMLHttpRequest"
            }


def get_url(name):
    return f"https://bastter.com/mercado/fii/{name}"


def get_cookies():
    return {
            "ASP.NET_SessionId": "vgs5dulw2azjbez4lsxn2xh0",
            "AtalhoFIIFiltro": "SouSocio",
            "Darkmode": "false",
            "NotificacoesExp": "1",
            "OrdemMural": "NaN",
            "SessionV2": "gRiVqFVyKVuuvKY_n-CYfha4x1VM_RtipcQ7jMatnGvuJ2ci8JVCu2rYzFeiO2lsB_k1ww2",
            "__AntiXsrfToken": "92881716a4414145ae9979ab5df4cadb",
            "__utma": "154587051.1410086461.1597002565.1597002565.1597131380.2",
            "__utmb": "154587051.7.10.1597131380",
            "__utmc": "154587051",
            "__utmt": "1",
            "__utmz": "154587051.1597002565.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
            "meuPrimeiroAcesso": "true"
                }
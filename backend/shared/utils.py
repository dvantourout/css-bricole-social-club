import logging
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

logger = logging.getLogger(__name__)

# Tracking parameters from https://maxchadwick.xyz/tracking-query-params-registry/
# This is the official community-maintained list (108 parameters)
TRACKING_PARAMS_REGISTRY = {
    # Facebook
    "fbclid",
    # Google Ads / Analytics / Shopping
    "gclid",
    "gclsrc",
    "gPromoCode",
    "gQT",
    "dclid",
    "gbraid",
    "wbraid",
    "gad_source",
    "gad_campaignid",
    "srsltid",
    # UTM Parameters (Google Analytics)
    "utm_content",
    "utm_term",
    "utm_campaign",
    "utm_medium",
    "utm_source",
    "utm_id",
    "utm_source_platform",
    "utm_creative_format",
    "utm_marketing_tactic",
    # Google Analytics
    "_ga",
    "_gl",
    # Twitter / X
    "twclid",
    # Yahoo / Yandex
    "yclid",
    # Email Marketing Platforms
    "mc_cid",
    "mc_eid",  # Mailchimp
    "_bta_tid",
    "_bta_c",  # Bronto
    "trk_contact",
    "trk_msg",
    "trk_module",
    "trk_sid",  # Listrak
    "dm_i",  # dotdigital
    # E-commerce Platforms
    "gdfms",
    "gdftrk",
    "gdffi",  # GoDataFeed
    # Klaviyo
    "_ke",
    "_kx",
    # Springbot
    "redirect_log_mongo_id",
    "redirect_mongo_id",
    "sb_referer_host",
    # Marin
    "mkwid",
    "pcrid",
    # Adobe
    "ef_id",  # Adobe Advertising Cloud
    "s_kwcid",  # Adobe Analytics
    # Microsoft Advertising
    "msclkid",
    # Pinterest
    "epik",
    # Analytics Platforms (Piwik/Matomo)
    "pk_campaign",
    "pk_kwd",
    "pk_keyword",
    "piwik_campaign",
    "piwik_kwd",
    "piwik_keyword",
    "mtm_campaign",
    "mtm_keyword",
    "mtm_source",
    "mtm_medium",
    "mtm_content",
    "mtm_cid",
    "mtm_group",
    "mtm_placement",
    "matomo_campaign",
    "matomo_keyword",
    "matomo_source",
    "matomo_medium",
    "matomo_content",
    "matomo_cid",
    "matomo_group",
    "matomo_placement",
    # HubSpot
    "hsa_cam",
    "hsa_grp",
    "hsa_mt",
    "hsa_src",
    "hsa_ad",
    "hsa_acc",
    "hsa_net",
    "hsa_kw",
    "hsa_tgt",
    "hsa_ver",
    # Branch
    "_branch_match_id",
    # eBay Partner Network
    "mkevt",
    "mkcid",
    "mkrid",
    "campid",
    "toolid",
    "customid",
    # Instagram
    "igshid",
    # Spotify / YouTube
    "si",
    # Wunderkind (formerly BounceExchange)
    "sms_source",
    "sms_click",
    "sms_uph",
    # TikTok
    "ttclid",
    # NextDoor
    "ndclid",
    # Snapchat
    "ScCid",
    # Rokt
    "rtid",
    # Impact (formerly Impact Radius)
    "irclickid",
    # Yahoo
    "vmcid",
    # Triple Whale
    "tw_source",
    "tw_campaign",
    "tw_term",
    "tw_content",
    "tw_adid",
    # Klar Insights
    "klar_source",
    "klar_cpid",
    "klar_adid",
}

TRACKING_PARAMS_CUSTOM = {
    "campaign",
    "expa",
    "utm_campaign",
    # awin1
    "utm_placement",
    "sv1",
    "sv_campaign_id",
    "awc",
    "source",
    "aw_affid",
    #
    "ref",
    "sPartner",
    "divacampaign",
}

TRACKING_PARAMS = TRACKING_PARAMS_REGISTRY | TRACKING_PARAMS_CUSTOM


def clean_affiliate(url: str) -> str | None:
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    # TODO: https://underarmourfr.sjv.io/
    # TODO: loaded.pxf.io
    if "murl" in query_params:
        return query_params.get("murl")[0]

    if "url" in query_params:
        return query_params.get("url")[0]

    # https://tc.tradetracker.net
    # https://loaded.pxf.io/
    # https://underarmourfr.sjv.io/
    if "u" in query_params:
        return query_params.get("u")[0]

    # https://track.webgains.com/
    if "wgtarget" in query_params:
        return query_params.get("wgtarget")[0]

    # https://jf79.net/c/?li=1801039&wi=358413&pid=1070d5a5457a5ff779dec9358f66bf35&dl=link%3Fid%3Dp5Zs8TJlngw%26offerid%3D1484571.42587293640119481389228%26type%3D15%26murl%3Dhttps%253A%252F%252Ffr.coach.com%252Ffr_FR%252Fproducts%252Fsac-%25C3%25A0-dos-crosby%252FCY279-B4%25252FBK.html&ws=%24%7BsubId%7D
    if parsed_url.netloc in {"jf79.net"}:
        if "dl" in query_params:
            dl_query_params = query_params.get("dl")[0]

            return clean_affiliate(dl_query_params)

    # TODO: make a list of all affiation sites
    # TODO: still save it to the db but mark it to be cleaned later
    # TODO: for awin, only p query paramter is mandatory, a and m
    # are not (probably for announcer and merchant?)
    if parsed_url.netloc in {
        "cmodul.solutenetwork.com",
        "www.awin1.com",
        "bdt9.net",
    }:
        logger.error(f"Uncleaned url: {parsed_url.netloc}")
        return None

    return url


def clean_link(url: str) -> str | None:
    logger.debug(f"cleaning url: {url}")

    url = clean_affiliate(url)

    if url is None or url and not url.startswith("http"):
        return None

    parsed_url = urlparse(url, allow_fragments=False)
    query_params = parse_qs(parsed_url.query)

    removed_params = {}
    cleaned_params = dict()

    for key, values in query_params.items():
        if key.lower() not in {p.lower() for p in TRACKING_PARAMS}:
            cleaned_params[key] = values
        else:
            removed_params[key] = values

    logger.info(f"removed params {removed_params}")
    logger.warning(f"kept params {cleaned_params}")

    new_query = urlencode(cleaned_params, doseq=True)

    cleaned_parsed = parsed_url._replace(query=new_query)

    return str(urlunparse(cleaned_parsed))

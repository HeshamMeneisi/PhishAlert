from whois import get_domain_age

def is_shorten(domain_part):
    url_shortens = ['goo.gl', 'bit.ly', 'tinyurl', 'tiny.cc', 'lc.chat', 'is.gd', 'soo.gd', 's2r.co', 'bc.vc', 'adf.ly']
    for url in url_shortens:
        if len(domain_part.split(url)) > 1:
            return True
    return False


def find_dash(domain_part):
    dash_split = domain_part.split('-')
    if len(dash_split) > 1:
        return True
    return False


def remove_www(url):
    new_url = ""
    www_split = url.split('www.')
    for term in www_split:
        new_url += term
    return new_url


def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def get_flags(url):
    url = remove_www(url)
    d_slash_split = url.split('//')
    http_part = d_slash_split[0]

    # check for https
    if http_part == "https:":
        http_flag = 1
    else:
        http_flag = -1
    if len(d_slash_split) > 1:
        web_part = d_slash_split[1]
    else:
        web_part = http_part

    # check for https in domain part
    if web_part[0:5] == "https":
        http_domain_flag = 1
        web_part = web_part[5:len(web_part)]
    else:
        http_domain_flag = -1

    # using ip address in domain part
    slash_split = web_part.split('/')
    domain_part = slash_split[0]
    dot_split = domain_part.split('.')
    ip_address_flag = -1
    for term in dot_split:
        if term.isdigit() or is_hex(term):
            ip_address_flag = 1

    # Sub Domain Flag
    subdomain_flag = -1
    if ip_address_flag == -1:
        if len(dot_split) == 3:
            # suspicious
            subdomain_flag = 0
        elif len(dot_split) > 3:
            subdomain_flag = 1

    # url length flag
    url_length_flag = -1
    if 54 <= len(url) <= 75:
        # suspicious
        url_length_flag = 0
    elif len(url) > 75:
        url_length_flag = 1

    # @ flag
    at_symbol_flag = -1
    for char in url:
        if char == '@':
            at_symbol_flag = 1

    # redirection flag
    redirection_flag = -1
    if len(d_slash_split) > 2:
        redirection_flag = 1

    # dash flag
    dash_flag = -1
    if find_dash(domain_part):
        dash_flag = 1

    # shorten flag
    shorten_flag = -1
    if is_shorten(domain_part):
        shorten_flag = 1

    domain_age_flag = 1
    age = get_domain_age(domain_part)
    if age <= 365:
        domain_age_flag = -1
        if(http_flag > 0):
            http_flag = 0

    return [ip_address_flag, url_length_flag, shorten_flag, at_symbol_flag,
            redirection_flag, dash_flag, subdomain_flag, http_flag, domain_age_flag, http_domain_flag]

# print(url_stripper('https://https-www-paypal-it-webapps-mpp-home.soft-hair.com/'))


import requests

from plotly.graph_objs import Bar
from plotly import offline

from datetime import datetime, timedelta


def rankings():
    # Make an API call and store the response.
    yesterday_raw = datetime.now() - timedelta(days=1)
    yesterday = yesterday_raw.strftime("%Y-%m-%d")
    corona_stats_ch_loc = f'/tmp/corona_stats_{yesterday}.html'
    url = f'https://covid19-rest.herokuapp.com/api/openzh/v1/country/CH?date={yesterday}'
    headers = {'Accept': ''}

    r = requests.get(url, headers)
    # Response object has an attribute called "status_code". 200: successful
    print(f"Status code: {r.status_code}")

    response_dict = r.json()
    kanton_list = response_dict['records']
    
    kanton_links, n_cases, n_deceaseds, case_labels, deceaseds_labels = [], [], [], [], []
    for kanton in kanton_list:
        #list of cantons with a reference to source information
        kanton_name = kanton['abbreviation_canton_and_fl']
        kanton_source = kanton['source']
        kanton_link = f"<a href='{kanton_source}'>{kanton_name}</a>"
        kanton_links.append(kanton_link)
        #list of nr of cumulative cases
        if kanton['ncumul_conf']:
            n_case = kanton['ncumul_conf']
        else:
            n_case = 0
        n_cases.append(n_case)
        case_labels.append(f"{kanton_name}<br />{n_case}")
        #list of nr of cumulative deceaseds
        if kanton['ncumul_deceased']:
            n_deceased = kanton['ncumul_deceased']
        else:
            n_deceased = 0
        n_deceaseds.append(n_deceased)
        deceaseds_labels.append(f"{kanton_name}<br />{n_deceased}")
        
    data = [{
        'type': 'bar',
        'x': kanton_links,
        'y': n_cases,
        'name': 'Confirmed Cases',
        # The marker settings shown here affect the design of the bars. We set a 
        # custom blue color for the bars and specify that they’ll be outlined with 
        # a dark gray line that’s 1.5 pixels wide. We also set the opacity of the 
        # bars to 0.6 to soften the appearance of the chart a little.
        'marker': {
            'color': 'rgb(30, 50, 70)',
            'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
        },
        'opacity': 0.6,
        'hovertext': case_labels,
        'yaxis': 'y',
        'offsetgroup': '1',
    }, {
        'type': 'bar',
        'x': kanton_links,
        'y': n_deceaseds,
        'name': 'Confirmed Deceaseds',
        # The marker settings shown here affect the design of the bars. We set a 
        # custom blue color for the bars and specify that they’ll be outlined with 
        # a dark gray line that’s 1.5 pixels wide. We also set the opacity of the 
        # bars to 0.6 to soften the appearance of the chart a little.
        'marker': {
            'color': 'rgb(90, 120, 160)',
            'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
        },
        'opacity': 0.6,
        'hovertext': deceaseds_labels,
        'yaxis': 'y2',
        'offsetgroup': '2',
    }]

    my_layout = {
        'title': 'COVID-19 Statistics per Canton in Switzerland',
        'titlefont': {'size': 28},
        'xaxis': {
            'title': 'Cantons',
            'titlefont': {'size': 24},
            'tickfont': {'size': 12},
            'categoryorder':'total descending'
        },
        'yaxis': {
            'title': 'Number of Confirmed Cases',
            'titlefont': {'size': 24},
            'tickfont': {'size': 12},
        },
        'yaxis2': {
            'title': 'Number of Confirmed Deceaseds',
            'titlefont': {'size': 24},
            'tickfont': {'size': 12},
            'overlaying': 'y',
            'side': 'right',
        },
    }

    fig = {'data': data, 'layout': my_layout}
    if response_dict['records']:
        return offline.plot(fig, filename=corona_stats_ch_loc, auto_open=False)  
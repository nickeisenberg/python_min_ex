import panel as pn
from panel.viewable import Viewer
import param
import pyarrow.parquet as pq
import numpy as np
from hvplot.ui import Controls

GEOM_KINDS = ['paths', 'polygons', 'points']
STATS_KINDS = [
    'hist', 'kde', 'boxwhisker', 'violin', 'heatmap', 'bar', 'barh'
]
TWOD_KINDS = [
    'bivariate', 'heatmap', 'hexbin', 'labels', 'vectorfield'
] + GEOM_KINDS

df = pq.read_table('./data/brownian_motion.parquet').to_pandas()

class Style(Controls):
    alpha = param.Magnitude(default=1)

class df_exp(Viewer):

    kind = param.Selector

    style = param.ClassSelector(class_=Style)

    def __panel__(self):
        return self._layout

    def __init__(self, df, **params):
        x, y = params.get('x'), params.get('y')
        if 'y' in params:
            if isinstance(params['y'], list):
                params['y_multi'] = params.pop('y') 
            else:
                params['y_multi'] = [params['y']]
        controller_params = {}
        controls = [
            p.class_
            for p in self.param.objects().values()
            if isinstance(p, param.ClassSelector)
            and issubclass(p.class_, Controls)
        ]
        for cls in controls:
            controller_params[cls] = {
                k: params.pop(k) for k, v in dict(params).items()
                if k in cls.param
            }
        super().__init__(**params)
        self._data = df
        self._controls = pn.Param(
            self.param, parameters=['kind'],
            sizing_mode='stretch_width', max_width=300, show_name=False,
        )
        self.param.watch(self._toggle_controls, 'kind')
        self._tabs = pn.Tabs(
            tabs_location='left', width=400
        )
           

    
    def _toggle_controls(self, event=None):
        # Control high-level parameters
        visible = True
        if event and event.new in ('table', 'dataset'):
            # parameters = ['kind', 'columns']
            parameters = ['kind']
            visible = False
        elif event and event.new in TWOD_KINDS:
            # parameters = ['kind', 'x', 'y', 'by', 'groupby']
            parameters = ['kind']
        elif event and event.new in ('hist', 'kde', 'density'):
            self.x = None
            # parameters = ['kind', 'y_multi', 'by', 'groupby']
            parameters = ['kind']
        else:
            # parameters = ['kind', 'x', 'y_multi', 'by', 'groupby']
            parameters = ['kind']
        self._controls.parameters = parameters

        # Control other tabs
        tabs = [('Fields', self._controls)]
        if visible:
            tabs += [
                ('Style', self.style),
            ]
            # if event and event.new not in (
            #     'area', 'kde', 'line', 'ohlc', 'rgb', 'step'
            # ):
            #     tabs.insert(5, ('Colormapping', self.colormapping))
        self._tabs[:] = tabs

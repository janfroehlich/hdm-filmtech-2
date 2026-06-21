import numpy as np
import plotly.graph_objects as go

# This function helps to display images pixel per pixel
def show(arr: np.ndarray, colorscale: str = "gray") -> None:
    """Display a 2D or RGB numpy array as a 1:1 pixel image."""
    import imageio.v3 as iio
    import base64

    # Extend image size if too small to display
    if min(arr.shape[0],arr.shape[1]) <= 10:
        arr = np.repeat( np.repeat(arr, 10, axis=0), 10, axis=1)
    
    # Limit to 0...1
    arr = np.clip(arr,0,1)

    # Switch RGB and gray cases 
    if arr.ndim == 2:
        height, width = arr.shape
        uint8 = (np.clip(arr, arr.min(), arr.max()) * 255).astype(np.uint8)
    elif arr.ndim == 3 and arr.shape[2] == 3:
        height, width = arr.shape[:2]
        uint8 = (np.clip(arr, 0, 1) * 255).astype(np.uint8)
    else:
        raise ValueError(f"Expected 2D or N×M×3 array, got shape {arr.shape}")

    png_bytes = iio.imwrite("<bytes>", uint8, plugin="pillow", extension=".png")
    source = "data:image/png;base64," + base64.b64encode(png_bytes).decode()

    fig = go.Figure(go.Image(source=source))
    fig.update_layout(
        width=width,
        height=height,
        margin=dict(t=0, b=0, l=0, r=0),
        xaxis=dict(visible=False, scaleanchor="y"),
        yaxis=dict(visible=False, autorange="reversed"),
        paper_bgcolor="black",
        plot_bgcolor="black",
    )
    fig.show(config={"responsive": False})



def show2(top: np.ndarray, start_color: float = 0.5) -> list:
    from IPython.display import display, HTML, clear_output
    clear_output(wait=True)
    import plotly.graph_objects as go
    import ipywidgets as widgets
    from IPython.display import display, HTML  

    display(HTML("""
    <style>
    .jp-OutputArea-output,
    .jp-OutputArea-output div,
    .jp-Cell-outputArea,
    .widget-output,
    .output_area,
    .cell-output-ipywidget-background {
        background: black !important;
        background-color: black !important;
    }
    </style>
    """))

    s = top.shape[0]
    test_color = [start_color]

    bot = np.full_like(top, test_color[0])
    img = np.vstack([top, bot]).astype(np.float32)
    height, width = img.shape

    fig = go.FigureWidget(go.Heatmap(
        z=(img * 255).astype(np.uint8),
        colorscale=[[0, "black"], [1, "white"]],
        showscale=False,
        zmin=0, zmax=255,
    ))

    fig.update_layout(
        width=width,
        height=height,
        margin=dict(t=0, b=0, l=0, r=0),
        xaxis=dict(visible=False, scaleanchor="y"),
        yaxis=dict(visible=False, autorange="reversed"),
        paper_bgcolor="black",
        plot_bgcolor="black",
    )

    label = widgets.Label(
        value=f"test_color = {test_color[0]:.4f}",
        style={"description_width": "0px"},
        layout=widgets.Layout(color="white"),
    )

    def step(delta):
        test_color[0] = min(1.0, max(0.0, test_color[0] + delta))
        bot = np.full_like(top, test_color[0])
        new_z = (np.vstack([top, bot]) * 255).astype(np.uint8)
        with fig.batch_update():
            fig.data[0].z = new_z
        label.value = f"test_color = {test_color[0]:.2f}"

    btn_minus = widgets.Button(description="−", layout=widgets.Layout(width="48px"),
                               style=widgets.ButtonStyle(button_color="#222", text_color="white"))
    btn_plus  = widgets.Button(description="+", layout=widgets.Layout(width="48px"),
                               style=widgets.ButtonStyle(button_color="#222", text_color="white"))
    btn_minus.on_click(lambda _: step(-1.0/255.0))
    btn_plus.on_click( lambda _: step(+1.0/255.0))

    ui = widgets.VBox(
        [widgets.HBox([btn_minus, btn_plus, label]), fig],
        layout=widgets.Layout(background_color="black", padding="4px")
    )
    display(ui)
    return test_color

def show_toggle(*images: np.ndarray) -> None:
    import ipywidgets as widgets
    from IPython.display import display, clear_output, Javascript, HTML
    import imageio.v3 as iio
    import base64

    idx = [0]

    def make_z(arr):
        return (np.clip(arr, 0, 1) * 255).astype(np.uint8)

    def to_b64(arr):
        png_bytes = iio.imwrite("<bytes>", make_z(arr), plugin="pillow", extension=".png")
        return "data:image/png;base64," + base64.b64encode(png_bytes).decode()

    frames = [to_b64(arr) for arr in images]

    first = images[0]
    height, width = first.shape[:2]

    fig = go.FigureWidget(go.Image(source=frames[0]))
    fig.update_layout(
        width=width, height=height,
        margin=dict(t=0, b=0, l=0, r=0),
        xaxis=dict(visible=False, scaleanchor="y"),
        yaxis=dict(visible=False, autorange="reversed"),
        paper_bgcolor="black", plot_bgcolor="black",
    )

    label = widgets.Label(
        value=f"Image 1 / {len(images)}",
        style={"description_width": "0px"},
        layout=widgets.Layout(color="white"),
    )

    def beep():
        display(Javascript("""
            const ctx = new AudioContext();
            const o = ctx.createOscillator();
            const g = ctx.createGain();
            o.connect(g); g.connect(ctx.destination);
            o.frequency.value = 880;
            g.gain.setValueAtTime(0.3, ctx.currentTime);
            g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.15);
            o.start(ctx.currentTime);
            o.stop(ctx.currentTime + 0.15);
        """))

    def show_idx(i):
        with fig.batch_update():
            fig.data[0].source = frames[i]
        label.value = f"Image {i+1} / {len(images)}"
        beep()

    def prev(_):
        idx[0] = (idx[0] - 1) % len(images)
        show_idx(idx[0])

    def next_(_):
        idx[0] = (idx[0] + 1) % len(images)
        show_idx(idx[0])

    black = widgets.Layout(background_color="black")

    btn_prev = widgets.Button(description="◀", layout=widgets.Layout(width="48px"),
                              style=widgets.ButtonStyle(button_color="#222", text_color="white"))
    btn_next = widgets.Button(description="▶", layout=widgets.Layout(width="48px"),
                              style=widgets.ButtonStyle(button_color="#222", text_color="white"))
    btn_prev.on_click(prev)
    btn_next.on_click(next_)

    ui = widgets.VBox(
        [widgets.HBox([btn_prev, btn_next, label], layout=black), fig],
        layout=widgets.Layout(background_color="black", padding="4px", width=f"{width}px")
    )

    clear_output(wait=True)
    display(HTML("""
    <style>
    .cell-output-ipywidget-background,
    .jp-OutputArea-output,
    .widget-vbox,
    .widget-hbox,
    .widget-label {
        background-color: black !important;
    }
    </style>
    """))
    display(ui)


 
def _img_to_uri(arr, max_px=None):
    """Float image (0..1) -> small base64 PNG data-URI for fast widget updates.
 
    Sending a compressed PNG string is far cheaper over the Jupyter comm than a
    raw uint8 `z` array, which is what makes live slider updates fast. `max_px`
    optionally caps the longest side (cheap integer striding) for extra speed.
    """
    import numpy as np
    import base64
    import imageio.v3 as iio
 
    arr = np.clip(np.asarray(arr, dtype=float), 0, 1)
    if max_px is not None:
        h, w = arr.shape[:2]
        step = max(1, int(np.ceil(max(h, w) / float(max_px))))
        if step > 1:
            arr = arr[::step, ::step]
    u8 = (arr * 255 + 0.5).astype(np.uint8)
    png = iio.imwrite("<bytes>", u8, plugin="pillow", extension=".png")
    return "data:image/png;base64," + base64.b64encode(png).decode()
 
 
def _sbs_layout(img_h, img_w, n_img, H_area=320):
    """Geometry so each image panel is exactly as tall as the (square) curve plot.
 
    The curve subplot is made square (side = H_area px) and every image column is
    sized H_area * (img_w/img_h) px, so – with no scaleanchor – the images fill the
    full plotting height (= the plot's height) without being distorted.
    """
    aspect = img_w / img_h                      # width / height
    t, b, l, rmar, gap = 24, 55, 60, 10, 26
    cols = 1 + n_img
    column_widths = [1.0] + [aspect] * n_img     # plot = 1 unit, each image = aspect units
    total = sum(column_widths)
    inner = H_area * total                       # combined column width in px
    fig_w = inner + (cols - 1) * gap + l + rmar
    fig_h = H_area + t + b
    hspace = gap / max(1.0, fig_w - l - rmar)
    # x (paper) of the curve subplot's right edge -> anchor the legend there
    legend_x = l / fig_w + (column_widths[0] / total) * (inner / fig_w) - 0.01
    return dict(column_widths=column_widths, hspace=hspace, fig_w=fig_w, fig_h=fig_h,
                margin=dict(t=t, b=b, l=l, r=rmar), legend_x=legend_x)
 
 
def plot_TM(x, y, img=None) -> None:
    """Plot a tone-mapping transfer function (OOTF) in log-log space.
 
    Plotly replacement for B_FT2_30_RGB_Display_Rendering_Plot_TM.m.
 
      * dotted red  : the unaltered source (y = x)
      * solid red   : the tone-mapped transfer function
      * green lines : sRGB-monitor limits (1 and 1/100)
      * cyan line   : digital-cinema black limit (1/1000)
 
    If `img` is given (an already display-ready RGB image, values in 0..1),
    the curve is drawn smaller on the left and the image beside it on the right.
    """
    import numpy as np
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
 
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    x0, x1 = float(x[0]), float(x[-1])
 
    side_by_side = img is not None
    if side_by_side:
        _img = np.clip(np.asarray(img, dtype=float), 0, 1)
        L = _sbs_layout(_img.shape[0], _img.shape[1], n_img=1)
        fig = make_subplots(rows=1, cols=2, column_widths=L["column_widths"],
                            horizontal_spacing=L["hspace"])
        col = 1
    else:
        fig = go.Figure()
        col = None
 
    def _add(trace):
        fig.add_trace(trace, row=1, col=col) if side_by_side else fig.add_trace(trace)
 
    # Unaltered OOTF (source) -> dotted red
    _add(go.Scatter(x=x, y=x, mode="lines",
                    line=dict(color="red", dash="dot"), name="Source"))
    # Tone-mapped OOTF -> solid red
    _add(go.Scatter(x=x, y=y, mode="lines",
                    line=dict(color="red"), name="ToneMapped"))
    # Display limits
    _add(go.Scatter(x=[x0, x1], y=[1/100, 1/100], mode="lines",
                    line=dict(color="green"), name="sRGB-Monitor Limits"))
    _add(go.Scatter(x=[x0, x1], y=[1/1000, 1/1000], mode="lines",
                    line=dict(color="cyan"), name="Digital Cinema Limits"))
    _add(go.Scatter(x=[x0, x1], y=[1, 1], mode="lines",
                    line=dict(color="green"), showlegend=False))  # upper sRGB limit (no legend)
 
    xax = dict(type="log", showgrid=True,
               title="HDR input (Peak white at 4 for this example)")
    yax = dict(type="log", showgrid=True, title="HDR output",
               range=[np.log10(1e-5), np.log10(10)])  # ylim([1e-5 10])
 
    if side_by_side:
        fig.update_xaxes(row=1, col=1, **xax)
        fig.update_yaxes(row=1, col=1, **yax)
 
        # Right: the image (no scaleanchor -> fills full height = plot height)
        z = (_img * 255).astype(np.uint8)
        fig.add_trace(go.Image(z=z), row=1, col=2)
        fig.update_xaxes(row=1, col=2, visible=False)
        fig.update_yaxes(row=1, col=2, visible=False, autorange="reversed")
 
        fig.update_layout(
            width=L["fig_w"], height=L["fig_h"], margin=L["margin"],
            # legend in the lower-right corner of the (left) plot
            legend=dict(x=L["legend_x"], y=0.02, xanchor="right", yanchor="bottom",
                        bgcolor="rgba(255,255,255,0.65)",
                        bordercolor="lightgray", borderwidth=1),
        )
    else:
        fig.update_xaxes(**xax)
        fig.update_yaxes(**yax)
        fig.update_layout(
            width=560, height=380,
            margin=dict(t=20, b=55, l=60, r=15),
            legend=dict(x=0.98, y=0.02, xanchor="right", yanchor="bottom",
                        bgcolor="rgba(255,255,255,0.65)",
                        bordercolor="lightgray", borderwidth=1),
        )
 
    fig.show(config={"responsive": False})
 
 
def plot_TM_interactive(tone_fn, rgb, params, linear2sRGB, clamp=None,
                        intensity=False, compare=False, x=None,
                        continuous_update=False, max_preview_px=700) -> None:
    """Interactive tone-curve + image with live sliders (seamless, no blanking).
 
    Built like `show2`: a single FigureWidget is created once and mutated in
    place with `batch_update`, so dragging a slider updates the curve and the
    image without the output ever going blank. That makes before/after
    comparison easy — just drag back and forth.
 
    Parameters
    ----------
    tone_fn   : callable. tone_fn(values, p1, p2, ...) -> tone-mapped LINEAR
                values (same shape as `values`). The extra positional args are
                taken from the sliders in the order of `params`.
    rgb       : linear HDR image, shape (H, W, 3).
    params    : dict {name: (min, max, step, default)} -> one slider each.
    linear2sRGB, clamp : the usual display helpers (clamp defaults to clip 0..1).
    intensity : if True, tone-map the luminance and rescale RGB keeping colour
                ratios (instead of per channel).
    compare   : if True, show BOTH the per-channel and the on-intensity result,
                side by side and synced to the same sliders.
    continuous_update : if True, update live while dragging; if False (default)
                update once on release — much smoother for heavy images.
    max_preview_px : cap the longest side of the displayed image (cheap integer
                striding) to keep updates fast. Set None for full resolution.
    """
    import numpy as np
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
 
    if clamp is None:
        clamp = lambda v: np.clip(v, 0, 1)
    if x is None:
        x = 2.0 ** np.arange(-12, 2.0 + 1e-9, 0.01)
    x = np.asarray(x, dtype=float)
    x0, x1 = float(x[0]), float(x[-1])
    eps = np.finfo(float).eps
    rgb = np.asarray(rgb, dtype=float)
    lum = 0.2125 * rgb[:, :, 0] + 0.7154 * rgb[:, :, 1] + 0.0721 * rgb[:, :, 2]
 
    # Which image panels to show
    def per_channel(vals):
        return linear2sRGB(clamp(tone_fn(rgb, *vals)))
 
    def on_intensity(vals):
        ldrLum = clamp(tone_fn(lum, *vals))
        img = (rgb / (lum[:, :, None] + eps)) * ldrLum[:, :, None]
        return linear2sRGB(img)
 
    if compare:
        panels = [("Per channel", per_channel), ("On intensity", on_intensity)]
    elif intensity:
        panels = [("On intensity", on_intensity)]
    else:
        panels = [("", per_channel)]
 
    n_img = len(panels)
    cols = 1 + n_img
    titles = [""] + [p[0] for p in panels]
    L = _sbs_layout(rgb.shape[0], rgb.shape[1], n_img)
 
    # Try the interactive path; fall back to a static render if widgets missing
    try:
        import ipywidgets as widgets
        from IPython.display import display
    except Exception:
        vals0 = [d for (_, _, _, d) in params.values()]
        plot_TM(x, clamp(tone_fn(x, *vals0)), panels[0][1](vals0))
        return
 
    fig = go.FigureWidget(make_subplots(rows=1, cols=cols,
                                        column_widths=L["column_widths"],
                                        horizontal_spacing=L["hspace"],
                                        subplot_titles=titles))
    # Curve traces (left)
    fig.add_trace(go.Scatter(x=x, y=x, mode="lines",
                  line=dict(color="red", dash="dot"), name="Source"), row=1, col=1)
    fig.add_trace(go.Scatter(x=x, y=x, mode="lines",
                  line=dict(color="red"), name="ToneMapped"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[x0, x1], y=[1/100, 1/100], mode="lines",
                  line=dict(color="green"), name="sRGB-Monitor Limits"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[x0, x1], y=[1/1000, 1/1000], mode="lines",
                  line=dict(color="cyan"), name="Digital Cinema Limits"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[x0, x1], y=[1, 1], mode="lines",
                  line=dict(color="green"), showlegend=False), row=1, col=1)
    # Image traces (right) — use a base64 PNG `source` (cheap to ship) not `z`
    blank = _img_to_uri(np.zeros((rgb.shape[0], rgb.shape[1], 3)), max_preview_px)
    img_idx = []
    for j in range(n_img):
        fig.add_trace(go.Image(source=blank), row=1, col=2 + j)
        img_idx.append(len(fig.data) - 1)
 
    fig.update_xaxes(row=1, col=1, type="log", showgrid=True,
                     title="HDR input")
    fig.update_yaxes(row=1, col=1, type="log", showgrid=True, title="HDR output",
                     range=[np.log10(1e-5), np.log10(10)])
    for j in range(n_img):
        c = 2 + j
        fig.update_xaxes(row=1, col=c, visible=False)
        fig.update_yaxes(row=1, col=c, visible=False, autorange="reversed")
 
    fig.update_layout(width=L["fig_w"], height=L["fig_h"], margin=L["margin"],
                      legend=dict(x=L["legend_x"], y=0.02, xanchor="right", yanchor="bottom",
                                  bgcolor="rgba(255,255,255,0.65)",
                                  bordercolor="lightgray", borderwidth=1))
 
    # Sliders
    sliders = []
    for name, (lo, hi, step, default) in params.items():
        sliders.append(widgets.FloatSlider(
            value=default, min=lo, max=hi, step=step, description=name,
            continuous_update=continuous_update, readout_format=".3g",
            style={"description_width": "initial"},
            layout=widgets.Layout(width="340px")))
 
    def render(*_):
        vals = [s.value for s in sliders]
        with fig.batch_update():
            fig.data[1].y = clamp(tone_fn(x, *vals))             # tone-mapped curve
            for j, (_, fn) in enumerate(panels):
                fig.data[img_idx[j]].source = _img_to_uri(fn(vals), max_preview_px)
 
    for s in sliders:
        s.observe(render, names="value")
    render()
 
    display(widgets.VBox([widgets.VBox(sliders), fig],
                         layout=widgets.Layout(padding="4px")))
 
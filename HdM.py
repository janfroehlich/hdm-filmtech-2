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

    
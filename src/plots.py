import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data import read_data
from config import Config

MAX_PER_ROW = 6
CATEGORY_SPACING = 2


def _assign_grid_positions(df: pd.DataFrame,
                           max_per_row: int = 6,
                           category_spacing: int = 2) -> pd.DataFrame:
    df = df.copy()
    df['xScatter'] = 0
    df['yScatter'] = 0

    sorted_categories = (
        df[['ChallengeRating', 'ChallengeRatingInt']]
        .drop_duplicates()
        .sort_values('ChallengeRatingInt')
        .reset_index(drop=True)
    )

    for i, row in sorted_categories.iterrows():
        category = row['ChallengeRating']
        cat_mask = df['ChallengeRating'] == category
        cat_indices = df[cat_mask].index

        x_offset = i * (max_per_row + category_spacing)

        for j, idx in enumerate(cat_indices):
            x = (j % max_per_row) + x_offset
            y = j // max_per_row
            df.at[idx, 'xScatter'] = x
            df.at[idx, 'yScatter'] = y

    return df


def _calculate_bucket_lines(df: pd.DataFrame) -> np.ndarray:
    config = Config()
    bucket_lines = []
    for cr in config.CHALLENGE_RATINGS:
        if cr in df["ChallengeRating"].to_list():
            x_min = df[df["ChallengeRating"] == cr]["xScatter"].min() - 1
            x_max = df[df["ChallengeRating"] == cr]["xScatter"].min() + 6
            y_min = -1
            y_max = 0.5
            bucket_lines.append([x_min, y_max, x_min, y_min])
            bucket_lines.append([x_min, y_min, x_max, y_min])
            bucket_lines.append([x_max, y_min, x_max, y_max])
    return np.array(bucket_lines)


def _calculate_bucket_labels(df: pd.DataFrame) -> dict:
    config = Config()
    bucket_labels = {}
    for cr in config.CHALLENGE_RATINGS:
        if cr in df["ChallengeRating"].to_list():
            x_pos = df[df["ChallengeRating"] == cr]["xScatter"].min() + 2.5
            y_pos = -1.5
            bucket_labels[cr] = np.array([x_pos, y_pos])
    return bucket_labels


def generate_challenge_rating_fig(df: pd.DataFrame) -> None:
    """
    Generate a scatter plot of monster Challenge Rating.
    """
    config = Config()

    df["TypeLower"] = df["Type"].str.lower()

    bucket_lines = _calculate_bucket_lines(df)
    bucket_labels = _calculate_bucket_labels(df)

    fig = px.scatter(df, x="xScatter", y="yScatter")
    fig.update_traces(
        marker=dict(size=5, color=config.MARKER_COLOR),
        hovertemplate="<b>%{customdata[0]}</b><br><i>%{customdata[3]} "
                      "%{customdata[1]}</i>"
                      "<br>CR: %{customdata[2]}<extra></extra>",
        customdata=df[["Name", "TypeLower", "ChallengeRating", "Size"]].values)
    for bucket_line in bucket_lines:
        fig.add_shape(
            type="line",
            x0=bucket_line[0], y0=bucket_line[1],
            x1=bucket_line[2], y1=bucket_line[3],
            line=dict(color="black", width=1)
            )
    for cr, label_pos in bucket_labels.items():
        fig.add_annotation(
            text=cr,
            xref="x", yref="y", x=label_pos[0], y=label_pos[1],
            showarrow=False, borderpad=0, align="center", xanchor="center",
            font=dict(size=12, color="black", family=config.FONT_STACK),
            borderwidth=0, yanchor="top")
    fig.add_annotation(
        text="Monsters by <b>Challenge Rating</b>",
        xref="paper", yref="paper", x=0.5, y=1.3, showarrow=False, borderpad=0,
        font=dict(size=14, color="black", family=config.FONT_STACK),
        align="center", xanchor="center", borderwidth=0)
    fig.update_layout(
        xaxis=dict(
            title=dict(text=""),
            automargin=False,
            range=(-2, 223),
            fixedrange=True,
            showticklabels=False,
            tickvals=[],
            showgrid=False,
            zeroline=False,
            ),
        yaxis=dict(
            range=(-4, 8),
            title=dict(text=""),
            automargin=False,
            fixedrange=True,
            showgrid=False,
            showticklabels=False,
            tickvals=[],
            zeroline=False,
            ),
        paper_bgcolor=config.BG_COLOR,
        plot_bgcolor=config.BG_COLOR,
        margin=dict(l=10, r=10, t=30, b=10),
        width=config.WIDTH,
        height=120,
        )

    fig.write_html(
        "reports/html/monster_cr.html",
        full_html=False, include_plotlyjs='cdn',
        config={
            "displayModeBar": False,
            })


def generate_challenge_rating_by_type_fig(df: pd.DataFrame) -> None:
    """
    Generate a scatter plot of monster Challenge Rating with a dropdown
    to highlight points by Type.
    """
    config = Config()

    df["TypeLower"] = df["Type"].str.lower()

    bucket_lines = _calculate_bucket_lines(df)
    bucket_labels = _calculate_bucket_labels(df)

    base_marker = dict(size=5, color=config.MARKER_COLOR)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["xScatter"],
        y=df["yScatter"],
        mode="markers",
        marker=base_marker,
        hovertemplate="<b>%{customdata[0]}</b><br><i>%{customdata[3]} "
                      "%{customdata[1]}</i>"
                      "<br>CR: %{customdata[2]}<extra></extra>",
        customdata=df[["Name", "TypeLower", "ChallengeRating", "Size"]].values,
        name="All",
        visible=True
    ))

    for t in config.MONSTER_TYPES:
        mask = df["Type"] == t
        highlight_color = "#0000ff"
        faded_color = config.MARKER_COLOR

        marker_colors = [highlight_color if m else faded_color for m in mask]

        fig.add_trace(go.Scatter(
            x=df["xScatter"],
            y=df["yScatter"],
            mode="markers",
            marker=dict(size=5, color=marker_colors),
            hovertemplate="<b>%{customdata[0]}</b><br><i>%{customdata[3]} "
                          "%{customdata[1]}</i>"
                          "<br>CR: %{customdata[2]}<extra></extra>",
            customdata=df[["Name", "TypeLower",
                           "ChallengeRating", "Size"]].values,
            name=t,
            visible=False
        ))

    buttons = [
        dict(label="All",
             method="update",
             args=[{"visible": [True] + [False] * len(config.MONSTER_TYPES)}])
    ]

    for i, t in enumerate(config.MONSTER_TYPES):
        visibility = [False] * (len(config.MONSTER_TYPES) + 1)
        visibility[i + 1] = True
        buttons.append(dict(
            label=t,
            method="update",
            args=[{"visible": visibility}]
        ))

    fig.update_layout(
        updatemenus=[
            dict(buttons=buttons,
                 direction="left",
                 showactive=True,
                 active=0,
                 x=1.0,
                 xanchor="right",
                 y=1.2,
                 yanchor="top",
                 bgcolor="white",
                 bordercolor="black",
                 borderwidth=0,
                 font=dict(family=config.FONT_STACK, size=12, color="black"),
                 pad={"r": 0, "t": 0},
                 )
        ]
    )

    for bucket_line in bucket_lines:
        fig.add_shape(
            type="line",
            x0=bucket_line[0], y0=bucket_line[1],
            x1=bucket_line[2], y1=bucket_line[3],
            line=dict(color="black", width=1)
        )
    for cr, label_pos in bucket_labels.items():
        fig.add_annotation(
            text=cr,
            xref="x", yref="y", x=label_pos[0], y=label_pos[1],
            showarrow=False, borderpad=0, align="center", xanchor="center",
            font=dict(size=12, color="black", family=config.FONT_STACK),
            borderwidth=0, yanchor="top")
    fig.add_annotation(
        text="Monsters by <b>Challenge Rating</b> and <b>Type</b>",
        xref="paper", yref="paper", x=0.5, y=1.3, showarrow=False, borderpad=0,
        font=dict(size=14, color="black", family=config.FONT_STACK),
        align="center", xanchor="center", borderwidth=0)

    fig.update_layout(
        xaxis=dict(
            title=dict(text=""),
            automargin=False,
            range=(-2, 223),
            fixedrange=True,
            showticklabels=False,
            tickvals=[],
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            range=(-4, 8),
            title=dict(text=""),
            automargin=False,
            fixedrange=True,
            showgrid=False,
            showticklabels=False,
            tickvals=[],
            zeroline=False,
        ),
        paper_bgcolor=config.BG_COLOR,
        plot_bgcolor=config.BG_COLOR,
        margin=dict(l=10, r=10, t=30, b=10),
        width=config.WIDTH,
        height=120,
    )

    fig.write_html(
        "reports/html/monster_cr_by_type.html",
        full_html=False, include_plotlyjs='cdn',
        config={
            "displayModeBar": False,
        })


def generate_challenge_rating_by_size_fig(df: pd.DataFrame) -> None:
    """
    Generate a scatter plot of monster Challenge Rating with a dropdown
    to highlight points by Size.
    """
    config = Config()

    df["TypeLower"] = df["Type"].str.lower()

    bucket_lines = _calculate_bucket_lines(df)
    bucket_labels = _calculate_bucket_labels(df)

    base_marker = dict(size=5, color=config.MARKER_COLOR)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["xScatter"],
        y=df["yScatter"],
        mode="markers",
        marker=base_marker,
        hovertemplate="<b>%{customdata[0]}</b><br><i>%{customdata[3]} "
                      "%{customdata[1]}</i>"
                      "<br>CR: %{customdata[2]}<extra></extra>",
        customdata=df[["Name", "TypeLower", "ChallengeRating", "Size"]].values,
        name="All",
        visible=True
    ))

    for s in config.SIZES:
        mask = df["Size"] == s
        highlight_color = "#0000ff"
        faded_color = config.MARKER_COLOR

        marker_colors = [highlight_color if m else faded_color for m in mask]

        fig.add_trace(go.Scatter(
            x=df["xScatter"],
            y=df["yScatter"],
            mode="markers",
            marker=dict(size=5, color=marker_colors),
            hovertemplate="<b>%{customdata[0]}</b><br><i>%{customdata[3]} "
                          "%{customdata[1]}</i>"
                          "<br>CR: %{customdata[2]}<extra></extra>",
            customdata=df[["Name", "TypeLower",
                           "ChallengeRating", "Size"]].values,
            name=s,
            visible=False
        ))

    buttons = [
        dict(label="All",
             method="update",
             args=[{"visible": [True] + [False] * len(config.SIZES)}])
    ]

    for i, s in enumerate(config.SIZES):
        visibility = [False] * (len(config.SIZES) + 1)
        visibility[i + 1] = True
        buttons.append(dict(
            label=s,
            method="update",
            args=[{"visible": visibility}]
        ))

    fig.update_layout(
        updatemenus=[
            dict(buttons=buttons,
                 direction="left",
                 showactive=True,
                 active=0,
                 x=1.0,
                 xanchor="right",
                 y=1.2,
                 yanchor="top",
                 bgcolor="white",
                 bordercolor="black",
                 borderwidth=0,
                 font=dict(family=config.FONT_STACK, size=12, color="black"),
                 pad={"r": 0, "t": 0},
                 )
        ]
    )

    for bucket_line in bucket_lines:
        fig.add_shape(
            type="line",
            x0=bucket_line[0], y0=bucket_line[1],
            x1=bucket_line[2], y1=bucket_line[3],
            line=dict(color="black", width=1)
        )
    for cr, label_pos in bucket_labels.items():
        fig.add_annotation(
            text=cr,
            xref="x", yref="y", x=label_pos[0], y=label_pos[1],
            showarrow=False, borderpad=0, align="center", xanchor="center",
            font=dict(size=12, color="black", family=config.FONT_STACK),
            borderwidth=0, yanchor="top")
    fig.add_annotation(
        text="Monsters by <b>Challenge Rating</b> and <b>Size</b>",
        xref="paper", yref="paper", x=0.5, y=1.3, showarrow=False, borderpad=0,
        font=dict(size=14, color="black", family=config.FONT_STACK),
        align="center", xanchor="center", borderwidth=0)

    fig.update_layout(
        xaxis=dict(
            title=dict(text=""),
            automargin=False,
            range=(-2, 223),
            fixedrange=True,
            showticklabels=False,
            tickvals=[],
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            range=(-4, 8),
            title=dict(text=""),
            automargin=False,
            fixedrange=True,
            showgrid=False,
            showticklabels=False,
            tickvals=[],
            zeroline=False,
        ),
        paper_bgcolor=config.BG_COLOR,
        plot_bgcolor=config.BG_COLOR,
        margin=dict(l=10, r=10, t=30, b=10),
        width=config.WIDTH,
        height=120,
    )

    fig.write_html(
        "reports/html/monster_cr_by_size.html",
        full_html=False, include_plotlyjs='cdn',
        config={
            "displayModeBar": False,
        })


def generate_ability_radar_fig(df: pd.DataFrame) -> None:
    config = Config()
    df["TypeLower"] = df["Type"].str.lower()
    fig = go.Figure()

    buttons = []
    for i, row in df.iterrows():
        row_t = pd.DataFrame({
            "Ability": [ability for ability in config.ABILITIES],
            "Value": [row[ability] for ability in config.ABILITIES]
        })
        row_t = pd.concat([row_t, row_t.iloc[[0]]], ignore_index=True)
        text = [row["Name"]] * len(row_t)
        fig.add_trace(go.Scatterpolar(
            theta=row_t["Ability"],
            r=row_t["Value"],
            marker={"color": "#0000ff"},
            visible=False,
            mode="lines+markers",
            name=row["Name"],
            fill="toself",
            line=dict(width=2),
            hovertemplate="<b>%{text}</b><br>%{theta}: %{r}<extra></extra>",
            text=text,
            ))

        visibility = [False] * len(df)
        visibility[i] = True
        buttons.append(dict(
            label=row["Name"],
            method="update",
            args=[{"visible": visibility}]
        ))

    fig.data[0].visible = True

    fig.add_annotation(
            text="<b>Ability Scores</b> of Monsters",
            xref="paper", yref="paper",
            x=0.5, y=1.2,
            showarrow=False,
            font=dict(size=14, color="black", family=config.FONT_STACK),
            align="center",
            xanchor="center",
            borderpad=0,
            borderwidth=0,
    )

    fig.update_layout(
        updatemenus=[
            dict(buttons=buttons,
                 direction="up",
                 showactive=True,
                 active=0,
                 x=0.5,
                 xanchor="center",
                 y=-0.1,
                 yanchor="top",
                 bgcolor="white",
                 bordercolor="black",
                 borderwidth=0,
                 font=dict(family=config.FONT_STACK, size=12, color="black"),
                 pad={"r": 0, "t": 0},
                 )
        ],
        polar=dict(
            bgcolor=config.BG_COLOR,
            radialaxis=dict(
                visible=True,
                range=[1, 31],
                showline=False,
                showticklabels=False,
                ticks='',
                gridcolor='black',
                ),
            angularaxis=dict(
                showline=False,
                showticklabels=True,
                ticks='',
                tickfont=dict(
                    family=config.FONT_STACK,
                    size=12,
                    color="black"),
                gridcolor="black",
                )
            ),
        margin=dict(t=50, l=450, b=50, r=450),
        paper_bgcolor=config.BG_COLOR,
        plot_bgcolor=config.BG_COLOR,
        width=config.WIDTH,
        height=300,
    )

    fig.write_html(
        "reports/html/monster_abilities_radar.html",
        full_html=False, include_plotlyjs='cdn',
        config={
            "displayModeBar": False,
        })


if __name__ == "__main__":
    df = _assign_grid_positions(read_data(), MAX_PER_ROW, CATEGORY_SPACING)
    generate_challenge_rating_fig(df)
    generate_challenge_rating_by_type_fig(df)
    generate_challenge_rating_by_size_fig(df)
    generate_ability_radar_fig(df)

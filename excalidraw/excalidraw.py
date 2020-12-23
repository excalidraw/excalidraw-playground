import json
import random
import hashlib
import copy

RND = 4

CANVAS = [
    "#ffffff",
    "#f8f9fa",
    "#f1f3f5",
    "#fff5f5",
    "#fff0f6",
    "#f8f0fc",
    "#f3f0ff",
    "#edf2ff",
    "#e7f5ff",
    "#e3fafc",
    "#e6fcf5",
    "#ebfbee",
    "#f4fce3",
    "#fff9db",
    "#fff4e6",
]

BACKGROUND = [
    "transparent",
    "#ced4da",
    "#868e96",
    "#fa5252",
    "#e64980",
    "#be4bdb",
    "#7950f2",
    "#4c6ef5",
    "#228be6",
    "#15aabf",
    "#12b886",
    "#40c057",
    "#82c91e",
    "#fab005",
    "#fd7e14",
]

STROKE = [
    "#000000",
    "#343a40",
    "#495057",
    "#c92a2a",
    "#a61e4d",
    "#862e9c",
    "#5f3dc4",
    "#364fc7",
    "#1864ab",
    "#0b7285",
    "#087f5b",
    "#2b8a3e",
    "#5c940d",
    "#e67700",
    "#d9480f",
]


def get_random_background():
    return random.choice(BACKGROUND)


# source: https://stackoverflow.com/a/46336730/8418
def bounding_box(points):
    x_coordinates, y_coordinates = zip(*points)
    return [
        (min(x_coordinates), min(y_coordinates)),
        (max(x_coordinates), max(y_coordinates)),
    ]


def width_height(box):
    return (
        round(box[1][0] - box[0][0], RND),
        round(box[1][1] - box[0][1], RND),
    )


class Excalidraw:
    def __init__(self):
        self.data = {
            "version": 2,
            "type": "excalidraw",
            "source": "py-excalidraw",
            "elements": [],
            "appState": {"viewBackgroundColor": CANVAS[0]},
        }

        self.lib = {"type": "excalidrawlib", "version": 1, "library": []}

        self.TEXT_HEIGHT = 25
        self.TITLE_WIDTH = 100

    def __new_element(
        self,
        element_type,
        angle=0,
        roughness=1,
        strokeWidth=1,
        fillStyle="hachure",
        strokeSharpness="sharp",
        **kargs,
    ):
        element = {
            "angle": angle,
            "fillStyle": fillStyle,
            "opacity": 100,
            "roughness": roughness,
            "seed": random.randint(1_000_000, 100_000_000),
            "strokeColor": STROKE[0],
            "strokeSharpness": strokeSharpness,
            "strokeWidth": strokeWidth,
            "type": element_type,
        }

        for arg in kargs:
            element[arg] = kargs[arg]

        return element

    def add_rectangle(
        self,
        x,
        y,
        width,
        height,
        strokeColor=STROKE[0],
        backgroundColor=BACKGROUND[0],
        **kargs,
    ):
        element = self.__new_element("rectangle", **kargs)
        element["x"] = x
        element["y"] = y
        element["width"] = width
        element["height"] = height
        element["strokeColor"] = strokeColor
        element["backgroundColor"] = backgroundColor
        self.add_element(element)

    def add_ellipse(
        self,
        x,
        y,
        width,
        height,
        strokeColor=STROKE[0],
        backgroundColor=BACKGROUND[0],
        **kargs,
    ):
        element = self.__new_element("ellipse", **kargs)
        element["x"] = x
        element["y"] = y
        element["width"] = width
        element["height"] = height
        element["strokeColor"] = strokeColor
        element["backgroundColor"] = backgroundColor
        self.add_element(element)

    def add_line(
        self,
        x,
        y,
        points,
        strokeColor=STROKE[0],
        backgroundColor=BACKGROUND[0],
        **kargs,
    ):
        element = self.__new_element("line", **kargs)
        element["x"] = x
        element["y"] = y
        element["points"] = points
        element["strokeColor"] = strokeColor
        element["backgroundColor"] = backgroundColor
        element["width"], element["height"] = width_height(bounding_box(points))
        self.add_element(element)

    def add_arrow(
        self,
        x,
        y,
        points,
        strokeColor=STROKE[0],
        backgroundColor=BACKGROUND[0],
        **kargs,
    ):
        element = self.__new_element("arrow", **kargs)
        element["x"] = x
        element["y"] = y
        element["points"] = points
        element["strokeColor"] = strokeColor
        element["backgroundColor"] = backgroundColor
        element["width"], element["height"] = width_height(bounding_box(points))
        self.add_element(element)

    def add_text(self, x, y, width, height, text, **kargs):
        element = self.__new_element("text", **kargs)
        element["x"] = x
        element["y"] = y
        element["width"] = width
        element["height"] = height
        element["text"] = text
        element["fontFamily"] = 1
        element["fontSize"] = 20
        element["verticalAlign"] = "middle"
        element["baseline"] = 18
        self.add_element(element)

    def add_chart_axis(self, csv, bar_width, max_height):
        self.load_data(csv)
        self.gap = bar_width / 8
        self.max_y = 0
        max_x = len(self.chart_data)
        width = max_x * bar_width

        for key, value in self.chart_data:
            self.max_y = max(self.max_y, value)

        x = 0
        for key, value in self.chart_data:
            self.add_text(
                x * bar_width + self.gap,
                self.gap,
                bar_width,
                self.TEXT_HEIGHT,
                key,
                textAlign="center",
            )
            x += 1

        self.add_arrow(0, 0, [[0, 0], [0, -max_height - bar_width]])
        self.add_arrow(0, 0, [[0, 0], [width + bar_width, 0]])
        self.add_line(
            0,
            -max_height - self.gap,
            [[0, 0], [width + bar_width, 0]],
            strokeStyle="dashed",
        )

        # Add title in the middle on top
        self.add_text(
            (width - self.TITLE_WIDTH) / 2,
            -max_height - self.TEXT_HEIGHT * 3,
            self.TITLE_WIDTH,
            self.TEXT_HEIGHT,
            self.title_y,
            textAlign="center",
        )

        # Add the max value on the y-axis
        self.add_text(
            -self.TITLE_WIDTH - self.gap * 2,
            -max_height - self.gap - self.TEXT_HEIGHT / 2,
            self.TITLE_WIDTH,
            self.TEXT_HEIGHT,
            str(int(self.max_y)),
            textAlign="right",
        )

        # Add 0 on the y-axis
        self.add_text(
            -self.TITLE_WIDTH - self.gap * 2,
            -self.TEXT_HEIGHT / 2,
            self.TITLE_WIDTH,
            self.TEXT_HEIGHT,
            str(0),
            textAlign="right",
        )

    def add_chart(self, csv, bar_width, max_height):
        self.add_chart_axis(csv, bar_width, max_height)
        x = 0
        color = get_random_background()

        for key, value in self.chart_data:
            self.add_rectangle(
                x * bar_width + self.gap,
                -self.gap,
                bar_width - self.gap,
                -value * (max_height / self.max_y),
                backgroundColor=color,
            )
            x += 1

    def load_data(self, csv):
        self.chart_data = []
        with open(csv, "r") as file:
            header = False
            for line in file.readlines():
                if not header:
                    self.title_x, self.title_y = line.replace("\n", "").split(",")
                    header = True
                else:
                    key, value = line.split(",")
                    self.chart_data.append([key, float(value)])

    def save_as(self, filename):
        filename = filename if filename.find(".") > -1 else f"{filename}.excalidraw"
        with open(filename, "w") as excalidraw_file:
            json.dump(self.data, excalidraw_file, indent=2, sort_keys=True)
        print(f"File saved {filename}")

    def save_as_lib(self, filename):
        filename = filename if filename.find(".") > -1 else f"{filename}.excalidrawlib"
        for element in self.data["elements"]:
            self.lib["library"].append([element])
        with open(filename, "w") as excalidraw_lib_file:
            json.dump(self.lib, excalidraw_lib_file, indent=2, sort_keys=True)
        print(f"File saved {filename}")

    def add_element(self, element):
        self.data["elements"].append(self.normalize_element(element))

    def normalize_element(self, element):
        if "width" in element:
            element["width"] = round(element["width"], RND)
        if "height" in element:
            element["height"] = round(element["height"], RND)
        if "x" in element:
            element["x"] = round(element["x"], RND)
        if "y" in element:
            element["y"] = round(element["y"], RND)
        if "points" in element:
            element["points"] = [
                [round(p[0], RND), round(p[1], RND)] for p in element["points"]
            ]

        # generate the ID based on the elements data, withouth the seed
        data = copy.copy(element)
        del data["seed"]
        element["id"] = hashlib.md5(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()

        return element

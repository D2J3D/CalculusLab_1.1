from manim import *
import math
import numpy as np
import sys
#manim -pql ./main.py Test
params = [str(x) for x in input("Params: ").split(" ")]
n = int(params[0])
e_type = str(params[1])
class Test(Scene):
    CONFIG = {
        "x_min": 0,
        "x_max": 1,
    }

    def construct(self):
        ax = Axes(
            x_range=[0,2, 0.5], y_range=[0, 1.25, 0.25], x_length=8 ,y_length=5,
            x_axis_config={"numbers_to_include":np.arange(0, 2)},
            y_axis_config={"numbers_to_include": np.arange(0, 1.25), "numbers_with_elongated_ticks": np.arange(0, 1.25), "font_size":15},
        ).add_coordinates()
        graph = ax.plot(lambda x : math.e**(-x),x_range=[0, 1],color=YELLOW_E,)
        graph1_lab = (
            MathTex("f(x) = {e}^{-x}")
            .next_to(ax,LEFT, buff=0.2)
            .set_color(WHITE)
            .scale(0.8))

        def find_dx(n):
            t = [k / n for k in range(n + 1)]  # равномерное разбиение
            dx = t[1] - t[0]
            return dx

        def find_integral_sum(n, e_type):
            e_type = str(e_type)
            t = [k / n for k in range(n + 1)]  # равномерное разбиение
            di_list = []
            di_list.append([t[0], t[1]])
            dx = t[1] - t[0]
            for i in range(1, len(t) - 1):
                di_list.append([t[i], t[i + 1]])
            if e_type == "right":
                eq_list = [math.e ** (-x[-1]) for x in di_list]  # оснащение (правая граница)
            elif e_type == "left":
                eq_list = [math.e ** (-x[0]) for x in di_list]
            else:
                eq_list = [math.e ** (-(x[0] + (x[1] - x[0])/2)) for x in di_list]
            integral_sum = sum([dx * f for f in eq_list])
            return integral_sum

        def draw_func():
            self.add(graph1_lab)
            self.play(
                LaggedStart(DrawBorderThenFill(ax)),
                run_time=2,
                lag_ratio=1,
            )
            self.play(
                Create(graph)
            )

            self.wait(0.25)

        def build_integral_recs(n, e_type):
            e_type = str(e_type)
            dx_list = [find_dx(n)]
            rectangles = VGroup(
                *[ax.get_riemann_rectangles(
                    graph=graph,
                    x_range=[0, 1],
                    stroke_width=0.01,
                    stroke_color=WHITE,
                    fill_opacity=0.5,
                    input_sample_type=str(e_type),
                    dx=dx
                )
                for dx in dx_list]
            )
            draw_func()

            n_dx = (
                Tex(f'For n = {n} and {e_type} equipment \n integral sum = {"{:.6f}".format(find_integral_sum(n, e_type))}')
                    .next_to(ax, UP)
                    .set_color(WHITE)
                    .scale(0.8))

            first_area = rectangles[0]
            self.play(LaggedStart(Create(first_area), run_time=1.5, lag_ratio=1))
            self.wait(0.5)
            for k in range(1, len(dx_list)):
                self.wait(0.5)
                new_area = rectangles[k]
                self.play(Transform(first_area, new_area), run_time=1)
            self.play(Write(n_dx), run_time=2.5)
            self.wait(1)
            self.wait()
        build_integral_recs(n, str(e_type))


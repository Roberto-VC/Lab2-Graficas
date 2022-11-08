from cgitb import text
from re import M
import random
from vector import *
from gl import *


def bounding_box(A, B, C):
    # Mira cual es la bounding box
    xs = [A.x, B.x, C.x]
    ys = [A.y, B.y, C.y]

    xs.sort()
    ys.sort()

    return xs[0], xs[-1], ys[0], ys[-1]


def cross(V1, V2):
    # Producto cruz
    return (
        V1.y * V2.z - V1.z * V2.y,
        V1.z * V2.x - V1.x * V2.z,
        V1.x * V2.y - V1.y * V2.x,
    )


def barycentric(A, B, C, P):
    # Se calculan las baricentricas
    cx, cy, cz = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x), V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )

    u = cx / cz
    v = cy / cz
    w = 1 - (cx + cy) / cz

    return (w, v, u)


print()


def main():

    d = 0
    scale_factor = (1, 1, 1)
    # transform_factor = (600,200,0)
    # roation_factor = (0,0,pi/6)

    transform_factor = (0, 0, 0)
    roation_factor = (pi / 7, 0, 0)
    side = 1000
    Zubat = Obj("sphere.obj")
    b = Bitmap(side, side)
    m = 0

    def shader(render, **kwargs):
        w, v, u = kwargs["bar"]
        A, B, C = kwargs["vertices"]
        y = kwargs["aaa"]
        x = kwargs["bbb"]
        nA, nB, nC = kwargs["normals"]
        L = V3(0, 0, 1)
        iA = nA.normalize() @ L.normalize()
        iB = nB.normalize() @ L.normalize()
        iC = nC.normalize() @ L.normalize()

        i = iA * w + iB * u + iC * v

        if y < (100 + random.randint(0, 25)):
            return (229, 234, 255)
        elif y < (200 + random.randint(0, 40)):
            return (108, 124, 198)
        elif y < (250 + random.randint(0, 10)) and x < (500 + random.randint(0, 10)):
            return (108, 124, 198)

        elif y > 500:
            return (229, 234, 255)
        else:
            return (75, 105, 246)

    def shader1(render, **kwargs):
        w, v, u = kwargs["bar"]
        A, B, C = kwargs["vertices"]
        y = kwargs["aaa"]
        x = kwargs["bbb"]
        nA, nB, nC = kwargs["normals"]
        L = V3(0, 0, 1)
        iA = nA.normalize() @ L.normalize()
        iB = nB.normalize() @ L.normalize()
        iC = nC.normalize() @ L.normalize()

        i = iA * w + iB * u + iC * v

        return (100,100,100)

    def shader2(render, **kwargs):
        w, v, u = kwargs["bar"]
        A, B, C = kwargs["vertices"]
        y = kwargs["aaa"]
        x = kwargs["bbb"]
        nA, nB, nC = kwargs["normals"]
        L = V3(0, 0, 1)
        iA = nA.normalize() @ L.normalize()
        iB = nB.normalize() @ L.normalize()
        iC = nC.normalize() @ L.normalize()

        i = iA * w + iB * u + iC * v

        return (100,100,100)

    print("Bienvenido al renderizador!\n")
    nombre = "Temp.bmp"
    b.lookAt(V3(0, 10, 20), V3(0, 0, 0), V3(0, 10, 0))
    b.clearColor(255, 0, 225)

    def transform_vertex(vertex):
        # Transforma el vertice
        augmented_vertex = Matrix([[vertex[0]], [vertex[1]], [vertex[2]], [1]])
        transformed_vertex = (
            b.Viewport * b.Projection * b.View * b.Model * augmented_vertex
        )

        transformed_vertex = V3(
            transformed_vertex.List[0][0],
            transformed_vertex.List[1][0],
            transformed_vertex.List[2][0],
            transformed_vertex.List[3][0],
        )
        return V3(
            transformed_vertex.x / transformed_vertex.w,
            transformed_vertex.y / transformed_vertex.w,
            transformed_vertex.z / transformed_vertex.w,
        )

    print()

    def triangle(A, B, C, verticesn=[]):

        # "Se crea la normal del triangulo para sacar la intensidad")

        # Escalas de grises y se crea el bounding box
        p, q, r, s = bounding_box(A, B, C)
        for x in range(round(p), round(q) + 1):
            for y in range(round(r), round(s) + 1):
                # Mira las baricentras del bounding
                try:
                    w, v, u = barycentric(A, B, C, V3(x, y))
                except:
                    continue
                if w < 0 or v < 0 or u < 0:
                    continue
                z = A.z * w + B.z * v + C.z * u
                # "Usa el z bugger para mostrar que esta adelante o atras"
                if (
                    x >= 0
                    and y >= 0
                    and x < len(b._zbuffer)
                    and y < len(b._zbuffer[0])
                    and b._zbuffer[x][y] < z
                ):
                    b._zbuffer[x][y] = z
                    # Hay un atributo vació del método en caso que no haya textura.
                    b._color = b.active_shader(
                        b,
                        aaa=y,
                        bbb=x,
                        bar=(w, v, u),
                        vertices=(A, B, C),
                        normals=(verticesn[0], verticesn[1], verticesn[2]),
                    )
                    # "En vez de escalas de grises, utiliza los colores de la textura")
                    # "Se pinta el punto"
                    if b._color == None:
                        continue
                    b.Vertex(x, y)

    def load_model(zubat):
        b.loadModelMatrix(transform_factor, scale_factor, roation_factor)
        vertext = []
        vertextt = []
        vertexn = []
        vertexnn = []
        d = 0
        for face in zubat.faces:
            d = d + 1
            # Mira los poligonos y cuantos veritces tiene
            if len(face) == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                # Se obtienen los vertices de la figura y los transforma.
                v1 = transform_vertex(zubat.vertices[f1])
                v2 = transform_vertex(zubat.vertices[f2])
                v3 = transform_vertex(zubat.vertices[f3])
                v4 = transform_vertex(zubat.vertices[f4])

                # Si hay texuta. Saca de la textura las caras y vertices respectivos

                fn1 = face[0][2] - 1
                fn2 = face[1][2] - 1
                fn3 = face[2][2] - 1
                fn4 = face[3][2] - 1

                vn1 = V3(
                    zubat.nvertices[fn1][0],
                    zubat.nvertices[fn1][1],
                    zubat.nvertices[fn1][2],
                )
                vn2 = V3(
                    zubat.nvertices[fn2][0],
                    zubat.nvertices[fn2][1],
                    zubat.nvertices[fn2][2],
                )
                vn3 = V3(
                    zubat.nvertices[fn3][0],
                    zubat.nvertices[fn3][1],
                    zubat.nvertices[fn3][2],
                )
                vn4 = V3(
                    zubat.nvertices[fn4][0],
                    zubat.nvertices[fn4][1],
                    zubat.nvertices[fn4][2],
                )

                vertexn = [vn1, vn2, vn3]
                vertexnn = [vn1, vn4, vn3]
                # Para los los de cuatro poligonos, utiliza don traingulos
                triangle(
                    V3(v1.x, v1.y, v1.z),
                    V3(v2.x, v2.y, v2.z),
                    V3(v3.x, v3.y, v3.z),
                    vertexn,
                )
                triangle(
                    V3(v1.x, v1.y, v1.z),
                    V3(v4.x, v4.y, v4.z),
                    V3(v3.x, v3.y, v3.z),
                    vertexnn,
                )
            else:

                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                v1 = transform_vertex(zubat.vertices[f1])
                v2 = transform_vertex(zubat.vertices[f2])
                v3 = transform_vertex(zubat.vertices[f3])

                fn1 = face[0][2] - 1
                fn2 = face[1][2] - 1
                fn3 = face[2][2] - 1

                vn1 = V3(
                    zubat.nvertices[fn1][0],
                    zubat.nvertices[fn1][1],
                    zubat.nvertices[fn1][2],
                )
                vn2 = V3(
                    zubat.nvertices[fn2][0],
                    zubat.nvertices[fn2][1],
                    zubat.nvertices[fn2][2],
                )
                vn3 = V3(
                    zubat.nvertices[fn3][0],
                    zubat.nvertices[fn3][1],
                    zubat.nvertices[fn3][2],
                )

                vertexn = [vn1, vn2, vn3]
                triangle(
                    V3(v3.x, v3.y, v3.z),
                    V3(v1.x, v1.y, v1.z),
                    V3(v2.x, v2.y, v2.z),
                    vertexn,
                )

    b.active_shader = shader
    load_model(Zubat)
    scale_factor = (0.5, 0.5, 0.5)
    transform_factor = (0.5,1,0)
    b.active_shader = shader1
    load_model(Zubat)
    scale_factor = (0.25, 0.25, 0.25)
    transform_factor = (-0.5,1,0)
    b.active_shader = shader2
    load_model(Zubat)
    

    b.write(nombre)


if __name__ == "__main__":
    main()

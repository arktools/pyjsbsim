#include "cpp_rect.h"

Rectangle::Rectangle() {
    x0 = y0 = x1 = y1 = 0;
}

Rectangle::Rectangle(int a, int b, int c, int d) {
    x0 = a;
    y0 = b;
    x1 = c;
    y1 = d;  
}

Rectangle::~Rectangle() {
}

int Rectangle::getLength() {
    return x1-x0;
}

int Rectangle::getHeight() {
    return y1-y0;
}

int Rectangle::getArea() {
    return getLength()*getHeight();
}

void Rectangle::move(int dx, int dy) {
    x0 += dx;
    x1 += dx;
    y0 += dy;
    y1 += dy;
}

Rectangle Rectangle::operator+(const Rectangle& other) {
    return Rectangle(x0 < other.x0 ? x0 : other.x0,
                     y0 < other.y0 ? y0 : other.y0,
                     x1 > other.x1 ? x1 : other.x1,
                     y1 > other.y1 ? y1 : other.y1);
}

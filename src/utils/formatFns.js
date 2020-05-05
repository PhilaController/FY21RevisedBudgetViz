import { format } from "d3-format";

export function formatFn(d) {
    let s = `$${format(",.3s")(Math.abs(d))
        .replace(/G/, "B")}`;
    if (d < 0) s = "\u2212" + s;
    return s;
}

export function netChangeFormatFn(d) {
    let s = formatFn(d);
    if (d > 0) s = "+" + s;
    return s;
}

export function percentFn(d) {
    let s = `${(100 * Math.abs(d)).toFixed(0)}%`;
    if (d < 0) s = "\u2212" + s;
    return s;
};
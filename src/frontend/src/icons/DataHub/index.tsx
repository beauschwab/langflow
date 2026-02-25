import React, { forwardRef } from "react";
import SvgDataHub from "./DataHub";

export const DataHubIcon = forwardRef<
  SVGSVGElement,
  React.PropsWithChildren<{}>
>((props, ref) => {
  return <SvgDataHub ref={ref} {...props} />;
});

import React, { forwardRef } from "react";
import SvgOutlook from "./Outlook";

export const OutlookIcon = forwardRef<
  SVGSVGElement,
  React.PropsWithChildren<{}>
>((props, ref) => {
  return <SvgOutlook ref={ref} {...props} />;
});

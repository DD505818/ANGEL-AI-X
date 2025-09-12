import Image from "next/image";
import type { ReactElement } from "react";

/**
 * HaloLogo lazily renders the ANGEL.AI logo image.
 */
export default function HaloLogo(): ReactElement {
  return (
    <Image
      src="/halo.svg"
      alt="ANGEL.AI logo"
      width={80}
      height={80}
      loading="lazy"
      priority={false}
    />
  );
}


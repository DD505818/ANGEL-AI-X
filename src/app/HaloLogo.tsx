import Image from 'next/image';
import type { FC } from 'react';

/**
 * HaloLogo lazily renders the ANGEL.AI logo image.
 */
const HaloLogo: FC = (): JSX.Element => (
  <Image src="/halo.svg" alt="ANGEL.AI logo" width={80} height={80} loading="lazy" />
);

export default HaloLogo;

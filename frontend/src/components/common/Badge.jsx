/**
 * Common Badge component
 */
import { SEVERITY_COLORS } from '../../utils/constants';

export default function Badge({ severity, children, className = '' }) {
  const colorClass = SEVERITY_COLORS[severity] || SEVERITY_COLORS.low;

  return (
    <span className={`badge ${colorClass} ${className}`}>
      {children}
    </span>
  );
}

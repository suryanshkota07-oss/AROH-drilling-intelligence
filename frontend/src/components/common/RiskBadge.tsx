import type { RiskLevel } from '../../types/domain'
export function RiskBadge({ level }: { level: RiskLevel }) { return <span className={`risk-badge risk-badge--${level}`}>{level}</span> }

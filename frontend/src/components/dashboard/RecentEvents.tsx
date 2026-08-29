import { Clock3 } from 'lucide-react'
import type { DrillingEvent } from '../../types/domain'
import { PanelHeader } from '../common/PanelHeader'
import { RiskBadge } from '../common/RiskBadge'
export function RecentEvents({ events }: { events: DrillingEvent[] }) { return <section className="panel recent-events"><PanelHeader title="Recent Drilling Events" detail="Latest activity from the demonstration stream" /><ol className="event-list">{events.map((event) => <li key={event.eventId}><div className="event-time"><Clock3 aria-hidden="true" size={15} />{event.timestamp}</div><div className="event-content"><div><strong>{event.eventType}</strong><RiskBadge level={event.severity} /></div><p>{event.summary}</p><span>{event.wellId.replace('DEMO-', '')} · {event.depth.toLocaleString()} m · {event.formation}</span></div></li>)}</ol></section> }

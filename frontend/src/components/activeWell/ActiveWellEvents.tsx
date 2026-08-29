import { Clock3 } from 'lucide-react'
import type { DrillingEvent } from '../../types/domain'
import { PanelHeader } from '../common/PanelHeader'
import { RiskBadge } from '../common/RiskBadge'
export function ActiveWellEvents({ events }: { events: DrillingEvent[] }) { return <section className="panel active-well-events"><PanelHeader title="Recent Events Timeline" detail="Latest synthetic drilling and correlation events" /><ol className="active-event-list">{events.map((event) => <li key={event.eventId}><div className="active-event-time"><Clock3 aria-hidden="true" size={14} />{event.timestamp}</div><div className="active-event-body"><div><strong>{event.eventType}</strong><RiskBadge level={event.severity} /></div><p>{event.summary}</p><span>{event.depth.toLocaleString()} m · {event.formation}</span></div></li>)}</ol></section> }

import { SortablePreferenceList } from './SortablePreferenceList';

interface CompactPreferenceGridProps {
  names: string[];
  prefs: Record<string, string[]>;
  onReorder: (person: string, newOrder: string[]) => void;
}

export function CompactPreferenceGrid({ names, prefs, onReorder }: CompactPreferenceGridProps) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-3 gap-3 pr-2">
      {names.map((name) => (
        <div key={name} className="min-w-0">
          <p className="text-xs font-medium mb-1 truncate">{name}</p>
          <SortablePreferenceList
            personName={name}
            items={prefs[name] ?? []}
            onReorder={onReorder}
          />
        </div>
      ))}
    </div>
  );
}

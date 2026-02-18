import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { X } from 'lucide-react';

interface PersonListProps {
  label: string;
  persons: string[];
  onAdd: (name: string) => void;
  onRemove: (name: string) => void;
}

export function PersonList({ label, persons, onAdd, onRemove }: PersonListProps) {
  const [name, setName] = useState('');

  function handleAdd() {
    const trimmed = name.trim();
    if (trimmed && !persons.includes(trimmed)) {
      onAdd(trimmed);
      setName('');
    }
  }

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-semibold">{label}</h3>
      <div className="flex gap-2">
        <Input
          value={name}
          onChange={(e) => setName(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleAdd()}
          placeholder={`Add ${label.toLowerCase().slice(0, -1)}...`}
          className="h-8 text-sm"
        />
        <Button size="sm" onClick={handleAdd} disabled={!name.trim()}>
          Add
        </Button>
      </div>
      <div className="flex flex-wrap gap-1">
        {persons.map((p) => (
          <span
            key={p}
            className="inline-flex items-center gap-1 rounded-full bg-secondary px-2.5 py-0.5 text-xs font-medium"
          >
            {p}
            <button
              onClick={() => onRemove(p)}
              className="text-muted-foreground hover:text-foreground"
              aria-label={`Remove ${p}`}
            >
              <X className="h-3 w-3" />
            </button>
          </span>
        ))}
      </div>
    </div>
  );
}

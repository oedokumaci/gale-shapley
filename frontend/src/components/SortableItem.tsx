import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { GripVertical } from 'lucide-react';

interface SortableItemProps {
  id: string;
  rank: number;
}

export function SortableItem({ id, rank }: SortableItemProps) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } =
    useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`flex items-center gap-1 rounded border bg-card px-1.5 py-1 text-xs ${
        isDragging ? 'opacity-50 shadow-lg' : ''
      }`}
    >
      <button
        {...attributes}
        {...listeners}
        className="cursor-grab text-muted-foreground hover:text-foreground active:cursor-grabbing shrink-0"
        aria-label={`Drag to reorder ${id}`}
      >
        <GripVertical className="h-3 w-3" />
      </button>
      <span className="text-muted-foreground text-[10px] w-3 shrink-0">{rank}.</span>
      <span className="font-medium truncate">{id}</span>
    </div>
  );
}

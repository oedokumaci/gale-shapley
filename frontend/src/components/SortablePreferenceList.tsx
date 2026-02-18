import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { SortableItem } from './SortableItem';

interface SortablePreferenceListProps {
  personName: string;
  items: string[];
  onReorder: (personName: string, newOrder: string[]) => void;
}

export function SortablePreferenceList({
  personName,
  items,
  onReorder,
}: SortablePreferenceListProps) {
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
  );

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    if (over && active.id !== over.id) {
      const oldIndex = items.indexOf(active.id as string);
      const newIndex = items.indexOf(over.id as string);
      onReorder(personName, arrayMove(items, oldIndex, newIndex));
    }
  }

  if (items.length === 0) {
    return <p className="text-xs text-muted-foreground italic">No preferences to rank</p>;
  }

  return (
    <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
      <SortableContext items={items} strategy={verticalListSortingStrategy}>
        <div className="flex flex-col gap-1">
          {items.map((item, index) => (
            <SortableItem key={item} id={item} rank={index + 1} />
          ))}
        </div>
      </SortableContext>
    </DndContext>
  );
}

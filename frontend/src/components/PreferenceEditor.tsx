import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { PersonList } from './PersonList';
import { SortablePreferenceList } from './SortablePreferenceList';

interface PreferenceEditorProps {
  proposerNames: string[];
  responderNames: string[];
  proposerPrefs: Record<string, string[]>;
  responderPrefs: Record<string, string[]>;
  onAddProposer: (name: string) => void;
  onRemoveProposer: (name: string) => void;
  onAddResponder: (name: string) => void;
  onRemoveResponder: (name: string) => void;
  onReorderProposerPref: (person: string, newOrder: string[]) => void;
  onReorderResponderPref: (person: string, newOrder: string[]) => void;
}

export function PreferenceEditor({
  proposerNames,
  responderNames,
  proposerPrefs,
  responderPrefs,
  onAddProposer,
  onRemoveProposer,
  onAddResponder,
  onRemoveResponder,
  onReorderProposerPref,
  onReorderResponderPref,
}: PreferenceEditorProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Proposers column */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-lg">Proposers</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <PersonList
            label="Proposers"
            persons={proposerNames}
            onAdd={onAddProposer}
            onRemove={onRemoveProposer}
          />
          {proposerNames.length > 0 && responderNames.length > 0 && (
            <>
              <Separator />
              <h4 className="text-sm font-semibold">
                Preference Rankings
                <span className="text-xs font-normal text-muted-foreground ml-1">
                  (drag to reorder)
                </span>
              </h4>
              <ScrollArea className="max-h-[400px]">
                <div className="space-y-4 pr-3">
                  {proposerNames.map((name) => (
                    <div key={name}>
                      <p className="text-sm font-medium mb-1">{name}&apos;s preferences:</p>
                      <SortablePreferenceList
                        personName={name}
                        items={proposerPrefs[name] ?? []}
                        onReorder={onReorderProposerPref}
                      />
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </>
          )}
        </CardContent>
      </Card>

      {/* Responders column */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-lg">Responders</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <PersonList
            label="Responders"
            persons={responderNames}
            onAdd={onAddResponder}
            onRemove={onRemoveResponder}
          />
          {proposerNames.length > 0 && responderNames.length > 0 && (
            <>
              <Separator />
              <h4 className="text-sm font-semibold">
                Preference Rankings
                <span className="text-xs font-normal text-muted-foreground ml-1">
                  (drag to reorder)
                </span>
              </h4>
              <ScrollArea className="max-h-[400px]">
                <div className="space-y-4 pr-3">
                  {responderNames.map((name) => (
                    <div key={name}>
                      <p className="text-sm font-medium mb-1">{name}&apos;s preferences:</p>
                      <SortablePreferenceList
                        personName={name}
                        items={responderPrefs[name] ?? []}
                        onReorder={onReorderResponderPref}
                      />
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

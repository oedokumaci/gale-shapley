import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { PersonList } from './PersonList';
import { CompactPreferenceGrid } from './CompactPreferenceGrid';
import type { PersonImages } from '@/types';

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
  personImages: PersonImages;
  onUploadImage: (name: string, file: File) => void;
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
  personImages,
  onUploadImage,
}: PreferenceEditorProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* Proposers column */}
      <Card>
        <CardHeader className="pb-2 px-4 pt-4">
          <CardTitle className="text-base">Proposers</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 px-4 pb-4">
          <PersonList
            label="Proposers"
            persons={proposerNames}
            onAdd={onAddProposer}
            onRemove={onRemoveProposer}
            images={personImages}
            onUploadImage={onUploadImage}
          />
          {proposerNames.length > 0 && responderNames.length > 0 && (
            <>
              <Separator />
              <h4 className="text-xs font-semibold">
                Preference Rankings
                <span className="text-[10px] font-normal text-muted-foreground ml-1">
                  (drag to reorder)
                </span>
              </h4>
              <ScrollArea className="max-h-[400px]">
                <CompactPreferenceGrid
                  names={proposerNames}
                  prefs={proposerPrefs}
                  onReorder={onReorderProposerPref}
                />
              </ScrollArea>
            </>
          )}
        </CardContent>
      </Card>

      {/* Responders column */}
      <Card>
        <CardHeader className="pb-2 px-4 pt-4">
          <CardTitle className="text-base">Responders</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 px-4 pb-4">
          <PersonList
            label="Responders"
            persons={responderNames}
            onAdd={onAddResponder}
            onRemove={onRemoveResponder}
            images={personImages}
            onUploadImage={onUploadImage}
          />
          {proposerNames.length > 0 && responderNames.length > 0 && (
            <>
              <Separator />
              <h4 className="text-xs font-semibold">
                Preference Rankings
                <span className="text-[10px] font-normal text-muted-foreground ml-1">
                  (drag to reorder)
                </span>
              </h4>
              <ScrollArea className="max-h-[400px]">
                <CompactPreferenceGrid
                  names={responderNames}
                  prefs={responderPrefs}
                  onReorder={onReorderResponderPref}
                />
              </ScrollArea>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

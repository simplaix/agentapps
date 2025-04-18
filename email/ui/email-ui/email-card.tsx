// components/email-ui/email-card.tsx
import { formatDistanceToNow } from 'date-fns/formatDistanceToNow';

import { cn } from '@/lib/utils';
import { EmailResult } from '@/agentapps/tools/local/email/types/email';
import { Button } from '@/components/ui/button';
import { Letter } from 'react-letter';
interface EmailCardProps {
  email: EmailResult;
  isSelected: boolean;
  onSelect: (email: EmailResult) => void;
  onMailDisplay: (email: EmailResult) => void; // Add this new prop
}

export function EmailCard({
  email,
  isSelected,
  onSelect,
  onMailDisplay
}: EmailCardProps) {
  const handleClick = () => {
    onSelect(email);
    onMailDisplay(email);
  };

  return (
    <Button
      className={cn(
        'flex flex-col items-start gap-2 rounded-lg border p-3 text-left text-sm transition-all hover:bg-accent h-auto bg-gray-100 text-black overflow-hidden',
        isSelected && 'bg-muted'
      )}
      onClick={handleClick}
    >
      <div className="flex w-full flex-col gap-1 min-w-0">
        <div className="flex items-center min-w-0">
          <div className="flex items-center gap-2">
            <div className="font-semibold">{email.from}</div>
          </div>
          <div
            className={cn(
              'ml-auto text-xs',
              isSelected ? 'text-foreground' : 'text-muted-foreground'
            )}
          >
            {formatDistanceToNow(new Date(email.date), {
              addSuffix: true,
            })}
          </div>
        </div>
        <div className="flex w-full text-xs font-medium overflow-hidden truncate whitespace-nowrap">
          {email.subject}
        </div>
      </div>
      <div className="text-xs text-muted-foreground font-normal overflow-hidden truncate w-full">
        <Letter html={email.snippet} />
      </div>
    </Button>
  );
}

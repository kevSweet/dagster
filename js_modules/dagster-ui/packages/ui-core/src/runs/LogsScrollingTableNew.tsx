import {Box, NonIdealState} from '@dagster-io/ui-components';
import {useVirtualizer} from '@tanstack/react-virtual';
import {useEffect, useRef} from 'react';

import {Structured, Unstructured} from './LogsRow';
import {ILogsScrollingTableProps, ListEmptyState, filterLogs} from './LogsScrollingTable';
import {ColumnWidthsProvider, Headers} from './LogsScrollingTableHeader';
import {Container, DynamicRowContainer, Inner} from '../ui/VirtualizedTable';

const BOTTOM_SCROLL_THRESHOLD_PX = 60;

export const LogsScrollingTableNew = (props: ILogsScrollingTableProps) => {
  const {filterStepKeys, metadata, filter, logs} = props;

  const parentRef = useRef<HTMLDivElement>(null);
  const pinToBottom = useRef(true);

  const {filteredNodes, textMatchNodes} = filterLogs(logs, filter, filterStepKeys);

  const virtualizer = useVirtualizer({
    count: filteredNodes.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 64,
    overscan: 20,
    paddingEnd: 40,
  });

  const totalHeight = virtualizer.getTotalSize();
  const items = virtualizer.getVirtualItems();

  // Determine whether the user has scrolled away from the bottom of the log list.
  // If so, we no longer pin to the bottom of the list as new logs arrive. If they
  // scroll back to the bottom, we go back to pinning.
  useEffect(() => {
    const parent = parentRef.current;

    const onScroll = () => {
      const totalHeight = virtualizer.getTotalSize();
      const rectHeight = virtualizer.scrollRect.height;
      const scrollOffset = virtualizer.scrollOffset;

      // If we're within a certain threshold of the maximum scroll depth, consider this
      // to mean that the user wants to pin scrolling to the bottom.
      const maxScrollOffset = totalHeight - rectHeight;
      const shouldPin = scrollOffset > maxScrollOffset - BOTTOM_SCROLL_THRESHOLD_PX;

      pinToBottom.current = shouldPin;
    };

    parent && parent.addEventListener('scroll', onScroll);
    return () => {
      parent && parent.removeEventListener('scroll', onScroll);
    };
  }, [virtualizer]);

  // If we should pin to the bottom, do so when the height of the virtualized table changes.
  useEffect(() => {
    if (pinToBottom.current) {
      virtualizer.scrollToOffset(totalHeight, {align: 'end'});
    }
  }, [totalHeight, virtualizer]);

  const content = () => {
    if (logs.loading) {
      return (
        <Box margin={{top: 32}}>
          <ListEmptyState>
            <NonIdealState icon="spinner" title="Fetching logs..." />
          </ListEmptyState>
        </Box>
      );
    }

    return (
      <Inner $totalHeight={totalHeight}>
        <DynamicRowContainer $start={items[0]?.start ?? 0}>
          {items.map(({index, key}) => {
            const node = filteredNodes[index]!;
            const textMatch = textMatchNodes.includes(node);
            const focusedTimeMatch = Number(node.timestamp) === filter.focusedTime;
            const highlighted = textMatch || focusedTimeMatch;

            const row =
              node.__typename === 'LogMessageEvent' ? (
                <Unstructured node={node} metadata={metadata} highlighted={highlighted} />
              ) : (
                <Structured node={node} metadata={metadata} highlighted={highlighted} />
              );

            return (
              <div
                ref={virtualizer.measureElement}
                key={key}
                data-index={index}
                style={{position: 'relative'}}
              >
                {row}
              </div>
            );
          })}
        </DynamicRowContainer>
      </Inner>
    );
  };

  return (
    <ColumnWidthsProvider>
      <Headers />
      <Container ref={parentRef}>{content()}</Container>
    </ColumnWidthsProvider>
  );
};

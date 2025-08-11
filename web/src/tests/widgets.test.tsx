import * as Widgets from '../components/widgets';

test('exports eight widgets', () => {
  expect(Object.keys(Widgets)).toHaveLength(8);
});

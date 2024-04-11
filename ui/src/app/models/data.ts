export type Data = {
  operation: 'write' | 'read';
  userId: string;
  braceletId: string;
  timestamp: number;
};

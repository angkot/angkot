interface WayList {
  [wayId: number]: number[];
}

interface BooleanMap {
  [b: number]: boolean;
}

interface AdjacencyList {
  [a: number]: BooleanMap;
}

interface NumberMap {
  [value: number]: number;
}

interface DistanceMatrix {
  [a: number]: NumberMap;
}

interface Pos {
  x: number;
  y: number;
}

interface PosMap {
  [value: number]: Pos;
}

interface Queue {
  size(): number;
  enqueue(value: number);
  dequeue(): number;
}

interface PriorityQueue extends Queue {
}

class SortPriorityQueue implements PriorityQueue {
  private data: number[];
  private valueMap: NumberMap;

  constructor(valueMap: NumberMap) {
    this.data = [];
    this.valueMap = valueMap;
  }

  public size(): number {
    return this.data.length;
  }

  public enqueue(obj: number) {
    this.data.push(obj);
  }

  public dequeue(): number {
    if (this.data.length === 0) return 0;

    this.data.sort.apply(this, this.comparator);
    var out = this.data.splice(0, 1);

    return out[0];
  }

  private comparator(a: number, b: number) {
    return this.valueMap[a] - this.valueMap[b];
  }
}

class RouteFinder {
  private ways: WayList;
  private edges: AdjacencyList;
  private distance: DistanceMatrix;

  constructor() {
    this.reset();
  }

  public reset() {
    this.ways = {};
    this.edges = {};
    this.distance = {};
  }

  public addWay(wayId: number, nodeList: number[], pos: PosMap) {
    if (this.ways[wayId]) return;

    this.ways[wayId] = nodeList;

    for (var i=0; i<nodeList.length-1; i++) {
      var a = nodeList[i];
      var b = nodeList[i+1];
      var pa = pos[a];
      var pb = pos[b];
      var distance = this.getDistance(pa, pb);
      this.addSegment(wayId, a, b, distance);
    }
  }

  private getDistance(pa: Pos, pb: Pos) {
    var dx = pa.x - pb.x;
    var dy = pa.y - pb.y;
    return Math.sqrt(dx*dx + dy*dy);
  }

  public removeWay(wayId: number) {
    var nodeList:number[] = this.ways[wayId];
    if (!nodeList) return;

    for (var i=0; i<nodeList.length-1; i++) {
      var a = nodeList[i];
      var b = nodeList[i+1];
      this.removeSegment(wayId, a, b);
    }

    delete this.ways[wayId];
  }

  private addSegment(wayId: number, a: number, b: number, distance: number) {
    if (!this.edges[a]) this.edges[a]= {};
    if (!this.edges[b]) this.edges[b] = {};
    this.edges[a][b] = true;
    this.edges[b][a] = true;

    if (!this.distance[a]) this.distance[a] = {};
    if (!this.distance[b]) this.distance[b] = {};
    this.distance[a][b] = distance;
    this.distance[b][a] = distance;
  }

  private removeSegment(wayId:number, a:number, b:number) {
    if (this.edges[a]) delete this.edges[a][b];
    if (this.edges[b]) delete this.edges[b][a];
    if (this.distance[a]) delete this.distance[a][b];
    if (this.distance[b]) delete this.distance[b][a];
  }

  public findRoute(src: number, dst: number): number[] {
      if (!this.edges[src] || !this.edges[dst]) return [];

      var distance: NumberMap = {};
      distance[src] = 0;

      var previous: NumberMap = {};
      previous[src] = src;

      var visited: BooleanMap = {};
      visited[src] = true;

      var queue: PriorityQueue = new SortPriorityQueue(distance);
      queue.enqueue(src);

      var limit = 10000;
      while (queue.size() > 0 && limit > 0) {
        limit -= 1;
        var curr = queue.dequeue();
        var dist = distance[curr];

        visited[curr] = true;

        var nextNodes = this.edges[curr];
        for (var next in nextNodes) {
          if (!visited[next]) {
            var distanceNext: number = distance[curr] + this.distance[curr][next];
            if (distance[next] === undefined || distance[next] > distanceNext) {
              if (distance[next] === undefined) {
                queue.enqueue(next);
              }
              distance[next] = distanceNext;
              previous[next] = curr;
            }
          }
        }
      }

      if (distance[dst] === undefined) return [];

      var n = dst;
      var path: number[] = [n|0];
      while (n != previous[n]) {
        n = previous[n];
        path.splice(0, 0, n|0);
      }

      return path;
  }
}




$fn=36;


module true_hole (d=1, L=10)
{
	union() {
		rotate(a=90, v=[1,0,0])
		cylinder(center=true, r=d/2, h=L);

		translate([0,0,d/2*sqrt(2)/2])
		rotate(a=45, v=[0,1,0])
		rotate(a=90, v=[1,0,0])
		cube(center=true, size=[d/2, d/2, L]);

	}
}

module tricube(w=1, h=1, l=1)
{
	translate([0, w, 0]) rotate(a=90, v=[1,0,0])
	linear_extrude(height=w) {
		polygon(points=[[0,0], [0,h], [l,0]]);
	}
}


module arc(h=1, r1=1, r2=2, a=90)
{
	difference() {
		cylinder(r=r2, h=h);
		union() {
				cylinder(r=r1, h=h);
				translate([0,-r2,0]) mirror([1,0,0]) cube(size=[r2,r2*2,h]);
				rotate(a=90-a, v=[0,0,1]) translate([-r2,0,0]) mirror([0,1,0]) cube(size=[r2*2,r2,h]);
		}
	}

}


module subarc(r=1, h=1)
{
	translate([r,r,0])
	rotate(a=180, v=[0,0,1])
	difference() {
		cube(size=[r,r,h]);
		cylinder(r=r, h=h);
	}
}

